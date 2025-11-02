# Root-level Makefile for Snipe-IT + Flask + Chrome Extension

# 🧰 Setup new developer environment
setup:
	powershell ./ops-scripts/bootstrap-windows.ps1

# 🧱 Flask API Docker build & run
flask-up:
	cd flask-middleware && docker build -t flask-api . && docker run -d -p 5000:5000 flask-api

# 🧹 Stop Flask API container
flask-down:
	docker stop flask-api || true && docker rm flask-api || true

# ☁️ Terraform plan & apply (development)
terraform-plan:
	cd infra && terraform init && terraform validate && terraform plan -var-file=envs/dev.tfvars

terraform-apply:
	cd infra && terraform apply -auto-approve -var-file=envs/dev.tfvars

# 🚦 Post-deploy smoke tests
smoke-test:
	bash tools/smoke-tests/run_health_checks.sh

# 🚀 Trigger Snipe-IT deployment via AWS SSM
deploy-snipeit:
	bash tools/deploy-scripts/deploy-snipeit-ssm.sh i-0abc12345 eu-west-2

# 🧪 Run Flask API unit tests
flask-test:
	cd flask-middleware && pytest -v

# 🧩 Validate Chrome extension
extension-lint:
	cd chrome-extension && npx eslint .

# 📦 Build Chrome extension zip for deployment
extension-build:
	cd chrome-extension/src && zip -r ../extension.zip *
