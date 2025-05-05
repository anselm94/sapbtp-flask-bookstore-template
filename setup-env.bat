@echo off
set "APP_NAME=sapbtp-flask-bookstore-srv"

REM Check if .env file exists, if not create it from .env.example
if not exist .env (
    copy .env.example .env
)

REM Retrieve environment properties and extract the `VCAP_SERVICES` JSON
for /f "delims=" %%A in ('cf app --guid %APP_NAME%') do set "APP_GUID=%%A"
for /f "delims=" %%B in ('cf curl "/v2/apps/%APP_GUID%/env" ^| jq -r ".system_env_json.VCAP_SERVICES"') do set "VCAP_SERVICES_JSON=%%B"

REM Remove newlines from the JSON string
set "VCAP_SERVICES_JSON=%VCAP_SERVICES_JSON:
=%"

REM Check if the VCAP_SERVICES line already exists in .env and remove it
findstr /b /c:"VCAP_SERVICES=" .env >nul && (findstr /v /b /c:"VCAP_SERVICES=" .env > .env.tmp && move /y .env.tmp .env)

REM Append the VCAP_SERVICES JSON to the .env file
echo VCAP_SERVICES="%VCAP_SERVICES_JSON%" >> .env
