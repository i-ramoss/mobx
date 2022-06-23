from datetime import datetime

from extensions import db
from models.tenant_model import Tenant
from shared.app_errors import AppError
from shared.responses import make_exception_response


""" Controller responsible for adding and deleting user endpoints """


def add_tenant(json_data):
    name = json_data["name"]
    email = json_data["email"]
    password = json_data["password"]
    phone = json_data["phone"]
    rent_contract_id = None

    # Where does it come from?
    if "rent_contract_id" in json_data:
        rent_contract_id = json_data["rent_contract_id"]

    tenant = Tenant.query.filter_by(email=email).first()

    if tenant is not None:
        raise AppError("Já existe um inquilino com estes dados.")

    tenant = Tenant(name, email, password, phone, rent_contract_id)

    try:
        db.session.add(tenant)
        db.session.commit()

    except Exception as error:
        return make_exception_response(
            description=error.__str__(), message="Não foi possível cadastrar o inqulino."
        )

    return tenant.transform_to_json()


def show_tenants():
    # Fetch all customer records
    try:
        tenants = Tenant.query.all()

    except Exception as error:
        return make_exception_response(
            description=error, message="Não foi possível listar os inquilinos."
        )

    tenants_in_json = []

    for tenant in tenants:
        tenants_in_json.append(tenant.transform_to_json())

    return tenants_in_json


def get_tenant_by_id(tenant_id):
    try:
        tenant = Tenant.find_by_id(tenant_id)

    except Exception as error:
        raise AppError(
            "Não foi possível buscar o inquilino.", description=error.__str__()
        )

    return tenant.transform_to_json()
