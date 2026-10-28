"""
register_azure_model.py - Azure Machine Learning Model Registration Workflow
Smart Agriculture: Real-Time Irrigation Prediction at the IoT Edge

Configured for Samarth Kale's Azure Workspace:
- Subscription: 6e2fed37-f192-4da5-9cc7-c4d5ede66b7f (Azure for Students)
- Resource Group: rg-ml-assignment
- Workspace: ml-assignment5-samarthkale
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "irrigation_model.joblib")
STATUS_FILE = os.path.join(BASE_DIR, "outputs", "azure_registration_status.json")

# Default settings detected from Samarth Kale's active Azure ML Studio session
DEFAULT_SUBSCRIPTION_ID = "6e2fed37-f192-4da5-9cc7-c4d5ede66b7f"
DEFAULT_RESOURCE_GROUP = "rg-ml-assignment"
DEFAULT_WORKSPACE_NAME = "ml-assignment5-samarthkale"


def get_azure_config(
    subscription_id: Optional[str] = None,
    resource_group: Optional[str] = None,
    workspace_name: Optional[str] = None
) -> Dict[str, str]:
    """Retrieves Azure ML workspace configuration with fallback to Samarth's workspace."""
    sub_id = subscription_id or os.getenv("AZURE_SUBSCRIPTION_ID") or DEFAULT_SUBSCRIPTION_ID
    rg = resource_group or os.getenv("AZURE_RESOURCE_GROUP") or DEFAULT_RESOURCE_GROUP
    ws = workspace_name or os.getenv("AZURE_WORKSPACE_NAME") or DEFAULT_WORKSPACE_NAME
    return {
        "subscription_id": sub_id,
        "resource_group": rg,
        "workspace_name": ws,
    }


def check_azure_status() -> Dict[str, Any]:
    """Checks Azure ML connection and registration status."""
    cfg = get_azure_config()
    last_receipt = None
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                last_receipt = json.load(f)
        except Exception:
            pass

    return {
        "is_configured": True,
        "subscription_id": cfg["subscription_id"],
        "resource_group": cfg["resource_group"],
        "workspace_name": cfg["workspace_name"],
        "model_file_exists": os.path.exists(MODEL_PATH),
        "model_path": MODEL_PATH,
        "last_receipt": last_receipt
    }


def record_status_receipt(status_data: Dict[str, Any]):
    """Records registration receipt to disk."""
    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
    with open(STATUS_FILE, "w") as f:
        json.dump(status_data, f, indent=4)


def get_authenticated_credential():
    """
    Attempts authentication sequentially:
    1. DefaultAzureCredential (CLI / Env / Managed Identity)
    2. InteractiveBrowserCredential (opens browser tab)
    3. DeviceCodeCredential (code prompt for browser)
    """
    from azure.identity import (
        DefaultAzureCredential,
        InteractiveBrowserCredential,
        DeviceCodeCredential
    )

    print("[AUTH] Attempting DefaultAzureCredential...")
    try:
        cred = DefaultAzureCredential()
        # Test token acquisition
        return cred
    except Exception as e:
        print(f"[AUTH] DefaultAzureCredential requires interactive login: {e}")

    print("[AUTH] Falling back to InteractiveBrowserCredential...")
    try:
        return InteractiveBrowserCredential()
    except Exception as e:
        print(f"[AUTH] InteractiveBrowserCredential failed: {e}")

    print("[AUTH] Falling back to DeviceCodeCredential...")
    return DeviceCodeCredential()


def register_model_to_azure(
    subscription_id: Optional[str] = None,
    resource_group: Optional[str] = None,
    workspace_name: Optional[str] = None,
    model_name: str = "smart-irrigation-edge-rf",
    model_version: Optional[str] = None,
    description: str = "Random Forest Classifier for Edge Irrigation Prediction"
) -> Dict[str, Any]:
    """Connects to Azure ML workspace and registers model artifact."""
    print("=" * 70)
    print("   Azure Machine Learning SDK v2: Model Registration Service")
    print("   Workspace: ml-assignment5-samarthkale | Author: Samarth Kale")
    print("=" * 70)

    if not os.path.exists(MODEL_PATH):
        err = f"Model artifact not found at {MODEL_PATH}. Run train_model.py first."
        print(f"[ERROR] {err}")
        return {"success": False, "status": "MODEL_FILE_MISSING", "error": err}

    cfg = get_azure_config(subscription_id, resource_group, workspace_name)

    print(f"\n[AZURE TARGET WORKSPACE]")
    print(f"  - Subscription ID: {cfg['subscription_id']}")
    print(f"  - Resource Group : {cfg['resource_group']}")
    print(f"  - Workspace Name : {cfg['workspace_name']}")
    print(f"  - Model File     : {MODEL_PATH} ({os.path.getsize(MODEL_PATH) / 1024:.1f} KB)")

    try:
        from azure.ai.ml import MLClient
        from azure.ai.ml.entities import Model
        from azure.ai.ml.constants import AssetTypes
        from azure.identity import (
            InteractiveBrowserCredential,
            DefaultAzureCredential,
            DeviceCodeCredential
        )
    except ImportError as e:
        err = f"Azure ML SDK v2 libraries missing: {e}"
        print(f"[ERROR] {err}")
        return {"success": False, "status": "DEPENDENCY_MISSING", "error": err}

    # Attempt connection with credentials
    ml_client = None
    auth_errors = []

    # Strategy 1: Interactive Browser Credential (best for local browser)
    try:
        print("\n[AZURE] Connecting using InteractiveBrowserCredential...")
        cred = InteractiveBrowserCredential()
        ml_client = MLClient(
            credential=cred,
            subscription_id=cfg["subscription_id"],
            resource_group_name=cfg["resource_group"],
            workspace_name=cfg["workspace_name"],
        )
        # Test call to verify client
        ws = ml_client.workspaces.get(cfg["workspace_name"])
        print(f"[AZURE SUCCESS] Connected to Workspace: {ws.display_name or ws.name}")
    except Exception as ex1:
        auth_errors.append(f"InteractiveBrowserCredential: {ex1}")
        print(f"[NOTE] Interactive browser login encountered: {ex1}")

        # Strategy 2: DefaultAzureCredential
        try:
            print("[AZURE] Trying DefaultAzureCredential...")
            cred = DefaultAzureCredential()
            ml_client = MLClient(
                credential=cred,
                subscription_id=cfg["subscription_id"],
                resource_group_name=cfg["resource_group"],
                workspace_name=cfg["workspace_name"],
            )
            ws = ml_client.workspaces.get(cfg["workspace_name"])
            print(f"[AZURE SUCCESS] Connected to Workspace: {ws.display_name or ws.name}")
        except Exception as ex2:
            auth_errors.append(f"DefaultAzureCredential: {ex2}")
            print(f"[NOTE] DefaultAzureCredential encountered: {ex2}")

            # Strategy 3: DeviceCodeCredential
            try:
                print("\n[AZURE] Opening Device Code Login...")
                print(">>> Follow the prompt below to authenticate via your browser <<<")
                cred = DeviceCodeCredential()
                ml_client = MLClient(
                    credential=cred,
                    subscription_id=cfg["subscription_id"],
                    resource_group_name=cfg["resource_group"],
                    workspace_name=cfg["workspace_name"],
                )
                ws = ml_client.workspaces.get(cfg["workspace_name"])
                print(f"[AZURE SUCCESS] Connected to Workspace: {ws.display_name or ws.name}")
            except Exception as ex3:
                auth_errors.append(f"DeviceCodeCredential: {ex3}")
                err = f"All authentication methods failed. Details: {auth_errors}"
                print(f"\n[AZURE ERROR] {err}")
                receipt = {
                    "success": False,
                    "status": "AUTH_FAILED",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "workspace": cfg["workspace_name"],
                    "error": str(ex3)
                }
                record_status_receipt(receipt)
                return receipt

    # Model Registration
    try:
        print(f"\n[AZURE] Packaging model asset '{model_name}'...")
        model_entity = Model(
            path=MODEL_PATH,
            name=model_name,
            version=model_version,
            description=description,
            type=AssetTypes.CUSTOM_MODEL,
            tags={
                "project": "smart-agriculture-edge",
                "framework": "scikit-learn",
                "author": "Samarth Kale",
                "accuracy": "88.2%",
                "precision": "90.2%",
                "runtime": "iot-edge-offline"
            }
        )

        print(f"[AZURE] Submitting model registration to '{cfg['workspace_name']}'...")
        registered_model = ml_client.models.create_or_update(model_entity)

        reg_name = registered_model.name
        reg_version = registered_model.version
        print(f"\n" + "=" * 70)
        print(f"🎉 [AZURE SUCCESS] Model Successfully Registered in Azure ML!")
        print(f"  - Model Name   : {reg_name}")
        print(f"  - Model Version: {reg_version}")
        print(f"  - Asset ID     : {registered_model.id}")
        print(f"  - Portal Studio: https://ml.azure.com/models/{reg_name}/{reg_version}")
        print("=" * 70)

        receipt = {
            "success": True,
            "status": "REGISTERED",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_name": reg_name,
            "model_version": reg_version,
            "model_id": registered_model.id,
            "workspace": cfg["workspace_name"],
            "resource_group": cfg["resource_group"],
            "portal_url": f"https://ml.azure.com/models/{reg_name}/{reg_version}"
        }
        record_status_receipt(receipt)
        return receipt

    except Exception as e:
        err = f"Model registration submission failed: {e}"
        print(f"\n[AZURE ERROR] {err}")
        receipt = {
            "success": False,
            "status": "REGISTRATION_FAILED",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "workspace": cfg["workspace_name"],
            "error": str(e)
        }
        record_status_receipt(receipt)
        return receipt


def main():
    parser = argparse.ArgumentParser(description="Register Smart Irrigation Model in Azure ML Workspace")
    parser.add_argument("--subscription-id", type=str, default=None)
    parser.add_argument("--resource-group", type=str, default=None)
    parser.add_argument("--workspace-name", type=str, default=None)
    parser.add_argument("--model-name", type=str, default="smart-irrigation-edge-rf")
    parser.add_argument("--model-version", type=str, default=None)
    args = parser.parse_args()

    register_model_to_azure(
        subscription_id=args.subscription_id,
        resource_group=args.resource_group,
        workspace_name=args.workspace_name,
        model_name=args.model_name,
        model_version=args.model_version
    )


if __name__ == "__main__":
    main()
