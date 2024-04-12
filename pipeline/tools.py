import os
import sys
import numpy as np
import requests
import re
import inspect
from urllib import parse
from .utils import get_logger


class ToolError(Exception):
    """
    ToolError is a custom exception class that is raised when an error occurs in a tool.
    ---
    """

    pass


class Tool:
    """
    A tool is a function that can be used by a ToolLLM. It exposes complex APIs through simple interfaces.
    ---
    """

    def __init__(self, name, description):
        """
        Initialize the tool with a name and description.
        ---
        Args:
        - name: Name of the tool
        - description: Description of the tool
        """

        self.name = name
        self.description = description
        self.logger = get_logger()

    def __call__(self, *args, **kwargs):
        """
        Call the tool with the given arguments and keyword arguments.
        ---
        Args:
        - *args: Positional arguments
        - **kwargs: Keyword arguments

        Returns:
        - result: Result of the tool
        """

        raise NotImplementedError("__call__() is not implemented in base class")

    def __str__(self):
        """
        Return a string representation of the tool.
        ---
        Returns:
        - str: String representation of the tool
        """
        args = f"{inspect.signature(self.__call__)}".replace("(", "(args: ")
        return f"{self.description} {args}"


class Answer(Tool):
    """
    The final answer tool allows providing the user with a final answer to the question.
    ---
    """

    def __init__(self):
        super().__init__("Answer", "Provide a final answer to a question.")

    def __call__(self, answer):
        pass


class Algebra(Tool):
    """
    The algebra tool allows solving algebraic equations.
    ---
    """

    def __init__(self):
        super().__init__("Algebra", "Solve algebraic equations using python (+ - * /).")

    def __call__(self, equation):
        """
        Solve an algebraic equation.
        ---
        Args:
        - equation: Equation to solve

        Returns:
        - solution: Solution to the equation
        """

        # Verify pattern
        regex_pattern = (
            r"^(\s*-?\s*(\d+(\.\d+)?)(\s*[\+\-\*\/]\s*-?\s*(\d+(\.\d+)?))*)+$"
        )
        if not re.match(regex_pattern, equation):
            raise ToolError(f"Invalid equation: {equation}")

        # Solving equation
        self.logger.debug(f"Solving equation {equation}")
        solution = eval(equation)
        result = f"{solution}"
        self.logger.debug(f"Result = {result}")

        # Returning solution
        return result


class Weather(Tool):
    """
    The weather tool allows looking up the current weather at a given location.
    ---
    """

    def __init__(self):
        super().__init__("Weather", "Get the current weather at a location.")

    def _get_location_coordinates(self, location):
        """
        Search for coordinates for a given location
        ---
        Args:
        - location: Location to search for coordinates for

        Returns:
        - coords: Coordinates (latitude, longitude) for the given location, or None if no coordinates could be found.
        """

        # Fetching coordinates for requested location
        self.logger.debug(f"Obtaining coordinates for location {location}")
        url = f"https://nominatim.openstreetmap.org/search?q={parse.quote(location)}&format=json&polygon=1&addressdetails=1"
        self.logger.debug(f"URL: {url}")
        response = requests.get(url)

        # Error handling
        if response.status_code != 200:
            raise ToolError(f"Error getting coordinates for location {location}")

        # Parsing data
        data = response.json()
        return data[0]["lat"], data[0]["lon"]

    def _get_weather_data(self, coords):
        """
        Get weather data for a given location
        ---
        Args:
        - coords: Coordinates (latitude, longitude) for the location to get weather data for

        Returns:
        - weather_data: Weather data for the given location, or None if no weather data could be found.
        """

        # Fetching weather data for requested coordinates
        lat, lon = coords
        self.logger.debug(f"Obtaining weather data for coordinates {lat}, {lon}")
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,wind_speed_10m"
        self.logger.debug(f"URL: {url}")
        response = requests.get(url)

        # Error handling exception
        if response.status_code != 200:
            raise ToolError(f"Error getting weather data for coordinates {lat}, {lon}")

        # Parsing data
        data = response.json()
        weather_data = data.get("current", {})
        weather_units = data.get("current_units", {})
        for key, value in weather_data.items():
            weather_data[key] = f"{value} ({weather_units.get(key, '')})"

        return weather_data

    def __call__(self, location):
        """
        Get weather data for a given location
        ---
        Args:
        - location: Location to get weather data for

        Returns:
        - weather_data: Weather data for the given location, or None if no weather data could be found.
        """

        # Get coordinates for the given location
        coords = self._get_location_coordinates(location)

        # Get weather data for the given coordinates
        weather_data = self._get_weather_data(coords)
        return weather_data


class Search(Tool):
    """
    The search tool allows searching for information about a keyword on DBPedia.
    ---
    """

    def __init__(self):
        super().__init__("Search", "Search for information about a keyword on DBPedia.")

    def _lookup_keyword_url(self, keyword: str):
        """
        Find DBPedia resource url for a given keyword
        ---
        Args:
        - keyword: Keyword to search for

        Returns:
        - resource_url: DBPedia resource url for the given keyword, or None if no resource could be found.
        """

        # Look up keyword with dbpedia api
        url = f"https://lookup.dbpedia.org/api/search?format=JSON&maxResults=1&query={parse.quote(keyword)}"
        response = requests.get(url)

        # Error handling
        if response.status_code != 200:
            raise ToolError(f"Error looking up keyword {keyword}")

        # Parsing results from data
        data = response.json()
        docs = data.get("docs", [])
        if not len(docs):
            raise ToolError(f"No results for keyword {keyword}")

        # Parsing resource from results
        resource = docs[0].get("resource", [])
        if not len(resource):
            raise ToolError(f"No resource for keyword {keyword}")

        keyword_url = resource[0]

        return keyword_url

    def _lookup_keyword_url_description(self, keyword_url):
        """
        Find description for a given keyword url
        ---
        Args:
        - keyword_url: Keyword url to search for

        Returns:
        - description: Description for the given keyword url, or None if no description could be found.
        """

        # Verify if keyword_url has valid format
        if not keyword_url.startswith("http"):
            raise ToolError(f"Invalid keyword_url {keyword_url}")

        # Look up keyword url description with dbpedia api
        ## Build query
        query = f"""
        SELECT *
        WHERE
        {{
            <{keyword_url}> rdfs:comment ?description.
            FILTER ( LANG(?description) = "en" )
        }} LIMIT 1
        """
        ## Remove whitespace
        query = re.sub(r"\s+", " ", query)
        self.logger.debug(f"Query: {query}")
        ## Build URL
        url = f"https://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query={parse.quote(query)}&format=application%2Fsparql-results%2Bjson&timeout=30000&signal_void=on&signal_unconnected=on"
        self.logger.debug(f"URL: {url}")

        # Request url
        response = requests.get(url)
        if response.status_code != 200:
            raise ToolError(f"Error looking up keyword url {keyword_url}")

        # Parse response
        data = response.json()
        results = data.get("results", {})
        bindings = results.get("bindings", [])
        if not len(bindings):
            raise ToolError(f"No bindings available for url {keyword_url}")

        # Parse description
        description = bindings[0].get("description", {}).get("value", None)

        return description

    def __call__(self, keyword):
        """
        Find description for a given keyword
        ---
        Args:
        - keyword: Keyword to search for

        Returns:
        - description: Description for the given keyword, or None if no description could be found.
        """

        # Obtain keyword url
        keyword_url = self._lookup_keyword_url(keyword)

        # Return keyword url description
        return self._lookup_keyword_url_description(keyword_url)


# Export dictionary with all available tools
tools = {
    "answer": Answer,
    "algebra": Algebra,
    "weather": Weather,
    "search": Search,
}
