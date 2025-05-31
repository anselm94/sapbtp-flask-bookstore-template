CF_API = https://api.cf.us10.hana.ondemand.com
CF_ORG = S4HANAD@S_sap-build-training-hcd2uswp
CF_SPACE = dev

.PHONY: update login build deploy undeploy

update:
	@echo "Upgrading the project NPM dependencies..."
	npx npm-check-updates -u
	npm install

	@echo "Upgrading the project Python dependencies..."
	cd srv
	poetry update --lock && poetry install
	cd ..

login:
	@echo "Logging into Cloud Foundry..."
	cf login -a $(CF_API) -o $(CF_ORG) -s $(CF_SPACE) --sso

build:
	@echo "Building the project with MBT..."
	mbt build

deploy:
	@echo "Deploying to Cloud Foundry using MBT..."
	cf deploy mta_archives/$(shell ls mta_archives | grep .mtar | tail -n 1)

undeploy:
	@echo "Undeploying from Cloud Foundry..."
	cf undeploy sapbtp-flask-bookstore --delete-services
