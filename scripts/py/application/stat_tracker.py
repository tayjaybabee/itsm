import json

stats = {
    "demographic": {
        "sensors": None,
        "location": {
            "region": None,
            "zip": None,
            "timezone": None
        },
        "household": {
            "occupants": None,
            "adults": None,
            "children": None,
            "pets": None,
        }

    },
    "applet_data": {
        "forecast": {
            "ds_api_calls": {
                "check_key": {
                    "fail": 0,
                    "success": 0,
                    "last_call_time": None
                },
                "check_weather": {
                    "fail": 0,
                    "success": 0,
                    "last_call_time": None
                },
            },
            "gui": {
                "ds_api_calls": {
                    "check_key": {
                        "fail": 0,
                        "success": 0,
                        "last_call_time": None
                    },
                    "check_weather": {
                        "fail": 0,
                        "success": 0,
                        "last_call_time": None
                    },
                },
                "ip_api_calls": {
                    "fail": 0,
                    "success": 0,
                    "last_call_time": None
                },
                "lasts": {
                    "last_start": None,
                    "last_exit": {
                        "time": None,
                        "status_code": None
                    }
                }

            }
        },
        "git_utils": {

        }
    }
}


def grab_stats():
