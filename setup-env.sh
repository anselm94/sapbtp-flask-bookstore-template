APP_NAME="sapbtp-flask-bookstore-srv"

# Check if .env file exists, if not create it from .env.example
if [ ! -f .env ]; then
    cp .env.example .env
fi

# Retrieve environment properties and extract the `VCAP_SERVICES` JSON
VCAP_SERVICES_JSON=$(cf curl "/v2/apps/$(cf app --guid $APP_NAME)/env" | jq -rj '.system_env_json.VCAP_SERVICES')

# Remove newlines from the JSON string
VCAP_SERVICES_JSON=$(echo "$VCAP_SERVICES_JSON" | tr -d '\n')

# Check if the VCAP_SERVICES line already exists in .env and remove it
if grep -q "^VCAP_SERVICES=" .env; then
    sed -i '' "/^VCAP_SERVICES=/d" .env
fi

# Append the VCAP_SERVICES JSON to the .env file
VCAP_SERVICES_JSON=$(echo $VCAP_SERVICES_JSON | jq -rj tostring)
echo "VCAP_SERVICES='${VCAP_SERVICES_JSON}'" >> .env
