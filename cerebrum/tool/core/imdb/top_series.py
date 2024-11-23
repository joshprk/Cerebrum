from cerebrum.tool.base import BaseRapidAPITool

from cerebrum.utils import get_from_env

import requests

class TopSeries(BaseRapidAPITool):
    def __init__(self):
        super().__init__()
        self.url = "https://imdb-top-100-movies.p.rapidapi.com/series/"
        self.host_name = "imdb-top-100-movies.p.rapidapi.com"

        self.api_key = get_from_env("RAPID_API_KEY")

    def run(self, params):
        start = int(params["start"]) if "start" in params else 1
        end = int(params["end"])
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host_name
        }
        response = requests.get(self.url, headers=headers).json()
        result = self.parse_result(response, start, end)
        return result


    def parse_result(self, response, start, end) -> str:
        result = []
        for i in range(start, end):
            item = response[i]
            result.append(f'{item["title"]}, {item["genre"]}, {item["rating"]}, published in {item["year"]}')

        return f"Top {start}-{end} series ranked by IMDB are: " + ";".join(result)

    def get_tool_call_format(self):
        tool_call_format = {
            "type": "function",
            "function": {
                "name": "imdb_top_series",
                "description": "Query the latest top start-to-end series ranked by Imdb",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "start": {
                            "type": "string",
                            "description": "start of the rank range of the Imdb series",
                            "default": "1"
                        },
                        "end": {
                            "type": "string",
                            "description": "end of the rank range of the Imdb series"
                        }
                    },
                    "required": [
                        "end"
                    ]
                }
            }
        }
        return tool_call_format
