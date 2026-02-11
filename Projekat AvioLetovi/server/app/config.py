class Config:
    SQLALCHEMY_DATABASE_URI = (
         "mssql+pyodbc://@localhost/dbAvioUsers"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "flight-service-key"
    JWT_ACCESS_TOKEN_EXPIRES = 3600
