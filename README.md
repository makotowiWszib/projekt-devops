## Azure (IaC + CD) bez subskrypcji

To repozytorium zawiera:
- Infrastrukturę jako kod (IaC) w Bicep dla Azure Container Registry (ACR) w katalogu `infra/`
- Workflow CD, który potrafi zbudować i wypchnąć obraz Dockera do ACR

Rzeczywiste wdrożenie nie jest wykonywane, ponieważ to konto nie posiada subskrypcji Azure.  
Aby umożliwić wdrażanie, należy skonfigurować sekrety w GitHub:

- `AZURE_CLIENT_ID`
- `AZURE_TENANT_ID`
- `AZURE_SUBSCRIPTION_ID`
- `ACR_NAME`
- `ACR_LOGIN_SERVER`

Bez tych sekretów zadanie CD jest celowo pomijane.
