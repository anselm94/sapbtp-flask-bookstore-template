# 🚀 **SAP BTP Flask Starter App**

### **Build Production-Ready Flask Apps on SAP BTP with Ease!**

---

## 🌟 **Introduction**

Welcome to the **SAP BTP Flask Starter App**! This repository is your one-stop solution for building and deploying production-grade Flask applications on SAP Business Technology Platform (BTP). With built-in support for **XSUAA authentication & authorization**, **HANA database integration**, and **MTA deployment**, this project is designed to help developers—both beginners and experts—hit the ground running. 🎉

---

## ✨ **Features**

- **🔒 XSUAA Authentication & Authorization**  
  Secure your app with SAP's XSUAA service for seamless authentication and role-based access control.

- **📦 MTA Deployment**  
  Effortlessly deploy your app using the [Multi-Target Application (MTA) framework](https://help.sap.com/docs/btp/sap-business-technology-platform/multitarget-applications-in-cloud-foundry-environment).

- **🛠️ HANA Integration**  
  Leverage SAP HANA for robust database management with SQLAlchemy and [`@sap/cds-dk`](https://www.npmjs.com/package/@sap/cds-dk) for HDI artifact generation.

- **⚡ Local & Production Configurations**  
  Automatically adapt to local or production environments with minimal setup by setting `FLASK_ENV` environment variable

- **📋 CF Logging**  
  Integrated Cloud Foundry logging for better observability using [`cf-python-logging-support`](https://github.com/SAP/cf-python-logging-support)

- **🚀 Gunicorn for Production**  
  Run your app with the high-performance [Gunicorn WSGI server](https://gunicorn.org/) in production.

- **🩺 Health Check Endpoint**  
  Monitor app and database liveliness via the `/health` endpoint.

---

## 🤔 **Why Use This Repository?**

- **Time-Saving**: Pre-configured for SAP BTP, so you can focus on building features.
- **Best Practices**: Implements industry standards for Flask apps.
- **Scalable**: Designed to grow with your application needs.
- **Beginner-Friendly**: Easy-to-follow setup and documentation.

---

## 🛠️ **Getting Started**

### **Pre-requisites**

1. Install [`poetry`](https://python-poetry.org/docs/#installation) for dependency management.
2. Install [CF CLI](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html).
3. Install [CF MTA Plugin](https://github.com/cloudfoundry/multiapps-cli-plugin).
4. Install [NodeJS](https://nodejs.org/en/download).

### **Setup Steps**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/anselm94/sapbtp-flask-bookstore.git
   cd sapbtp-flask-bookstore
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Build the MTA Project**

   ```bash
   mbt build
   ```

4. **Deploy to Cloud Foundry**

   ```bash
   cf deploy mta_archives/sapbtp-flask-bookstore_1.0.0.mtar
   ```

5. **Configure Local Environment**

   - Copy `.env.example` to `.env`.
   - Run the setup script to populate `VCAP_SERVICES`:
     ```bash
     sh setup-env.sh
     ```

6. **Run the App Locally**

   ```bash
   cd srv
   flask run
   ```

7. **Test the API**
   - Use Postman or any API client to hit:  
     `http://127.0.0.1:5000/books` with OAuth2 'Client Credentials'.
   - For health check, access:  
     `http://127.0.0.1:5000/health` (no auth required).

---

## 📂 **Project Structure**

```plaintext
sapbtp-flask-bookstore/
├── db/                          # CDS schema and data files
│   ├── schema.cds               # Core Data Services (CDS) schema definition
│   ├── data/                    # Sample data for the database
├── gen/                         # Generated HANA artifacts
├── srv/                         # Flask application source code
│   ├── app.py                   # Entry point for the Flask application
│   ├── config.py                # Configuration management for different environments
│   ├── app/                     # Application modules
│   │   ├── database.py          # Database connection and setup logic
│   │   ├── models.py            # ORM models for database tables
│   │   ├── routes/              # API route definitions
│   │   │   ├── __init__.py      # Route initialization
│   │   ├── services/            # Business logic and service layer
│   │   │   ├── books_service.py # Service logic for book-related operations
│   ├── utils/                   # Utility functions for authentication and error handling
│   │   ├── auth_utils.py        # Authentication helper functions
|   │   ├── heathcheck_utils.py  # Healthcheck helper functions
├── mta.yaml                     # MTA deployment descriptor
├── setup-env.sh                 # Script to configure local environment
└── README.md                    # Project documentation
```

---

## 🔍 **How It Works**

1. **Authentication & Authorization**

   - Uses SAP XSUAA for OAuth2-based authentication & authorization - See [`srv/app/routes/__init__.py`](srv/app/routes/__init__.py)
   - Role-based access control is defined in [`xs-security.json`](./xs-security.json).

2. **Database Integration**

   - CDS models ([`db/schema.cds`](./db/schema.cds)) are converted to HANA HDI artifacts using [`@sap/cds-dk`](https://www.npmjs.com/package/@sap/cds-dk).
   - [SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/) is used for ORM mapping in the Flask app ([`srv/app/models.py`](./srv/app/models.py)) using [SAP HANA dialect](https://github.com/SAP/sqlalchemy-hana).

3. **Deployment**
   - MTA framework bundles the app, database, and services for deployment.
   - [`cf deploy`](https://docs.cloudfoundry.org/devguide/deploy-apps.html) handles the deployment to SAP BTP.

---

## 🧑‍💻 **Development Workflow**

- **Debugging**: Use VS Code's built-in debugger with the provided `launch.json`.
- **Extending**: Add new routes in [`srv/app/routes/`](./srv/app/routes/) and services in [`srv/app/services/`](./srv/app/services/).

---

## 📜 **License**

This project is licensed under the [MIT License](./LICENSE).

---

## 🙌 **Acknowledgments**

Special thanks to the SAP BTP community and contributors for their support and inspiration!
