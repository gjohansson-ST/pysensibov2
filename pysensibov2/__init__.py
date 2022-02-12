"""Python API for Sensibo."""
from __future__ import annotations
import json

from typing import Any
from aiohttp import ClientSession

from .exceptions import SensiboError, AuthenticationError

APIV1 = "https://home.sensibo.com/api/v1"
APIV2 = "https://home.sensibo.com/api/v2"


class SensiboClient(object):
    """Sensibo client."""

    def __init__(self, api_key: str, session: ClientSession | None = None):
        """Constructor.

        api_key: Key from https://home.sensibo.com/me/api
        session: aiohttp.ClientSession or None to create a new session.
        """
        self.api_key = api_key
        self._session = session if session else ClientSession()

    async def async_get_devices(self, fields: str = "*"):
        """Get all devices."""
        params = {"apiKey": self.api_key, "fields": fields}
        return await self._get("/users/me/pods", params)

    async def async_get_device(self, uid: str, fields: str = "*"):
        """Get specific device by UID."""
        params = {"apiKey": self.api_key, "fields": fields}
        return await self._get("/pods/{}".format(uid), params)

    async def async_get_climate_react(self, uid: str):
        """Get measurements of a device."""
        params = {"apiKey": self.api_key}
        return await self._get("/pods/{}/smartmode".format(uid), params)

    async def async_set_climate_react(self, uid: str, data: dict[str, bool]):
        """Get measurements of a device."""
        params = {"apiKey": self.api_key}
        return await self._put("/pods/{}/smartmode".format(uid), params, data)

    async def async_get_schedules(self, uid: str):
        """Get measurements of a device."""
        params = {"apiKey": self.api_key}
        return await self._get("/pods/{}/schedules/".format(uid), params)

    async def async_set_ac_states(
        self,
        uid: str,
        acstate: dict[str, bool | int | str],
    ):
        """Set a specific device property."""
        params = {"apiKey": self.api_key}
        data = {"acState": acstate}
        return await self._post("/pods/{}/acStates".format(uid), params, data)

    async def async_set_ac_state_property(
        self,
        uid: str,
        name: str,
        value: bool | int | str,
        ac_state: dict[str,Any],
        assumed_state: bool = False,
    ):
        """Set a specific device property."""
        params = {"apiKey": self.api_key}
        data = {"currentAcState": ac_state, "newValue": value}
        if assumed_state:
            data["reason"] = "StateCorrectionByUser"
        return await self._patch("/pods/{}/acStates/{}".format(uid, name), params, data)

    async def _get(self, path: str, params: dict[str, Any]):
        """Make api call to Sensibo api."""
        async with self._session.get(APIV2 + path, params=params) as resp:
            if resp.status == 401:
                raise AuthenticationError("Invalid API key")
            if resp.status != 200:
                error = await resp.text()
                raise SensiboError(f"API error: {error}")
            response = await resp.json()
        return response["result"]

    async def _put(self, path: str, params: dict[str, Any], data: dict[str, Any]):
        """Make api call to Sensibo api."""
        async with self._session.put(APIV2 + path, params=params, data=json.dumps(data)) as resp:
            if resp.status == 401:
                raise AuthenticationError("Invalid API key")
            if resp.status != 200:
                error = await resp.text()
                raise SensiboError(f"API error: {error}")
            response = await resp.json()
        return response["result"]

    async def _post(self, path: str, params: dict[str, Any], data: dict[str, Any]):
        """Make api call to Sensibo api."""
        async with self._session.post(APIV2 + path, params=params, data=json.dumps(data)) as resp:
            if resp.status == 401:
                raise AuthenticationError("Invalid API key")
            if resp.status != 200:
                error = await resp.text()
                raise SensiboError(f"API error: {error}")
            response = await resp.json()
        return response["result"]

    async def _patch(self, path: str, params: dict[str, Any], data: dict[str, Any]):
        """Make api call to Sensibo api."""
        async with self._session.patch(APIV2 + path, params=params, data=json.dumps(data)) as resp:
            if resp.status == 401:
                raise AuthenticationError("Invalid API key")
            if resp.status != 200:
                error = await resp.text()
                raise SensiboError(f"API error: {error}")
            response = await resp.json()
        return response["result"]
