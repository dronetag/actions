# dronetag/actions/build-push-acr

**build-push-acr** action builds a Docker image using the project's Dockerfile and pushes it to an Azure Container Registry (ACR) repository.

It supports tagging the image, passing build arguments and secrets, and optionally forwarding SSH sockets.

## Inputs

- **`tags`** (optional): Tags for the Docker image. Defaults to `latest`.
- **`repository-name`** (required): Name of the repository in ACR.
- **`acr-login-server`** (optional): ACR login server. Defaults to `dronetag.azurecr.io`.
- **`acr-username`** (required): Username for ACR authentication.
- **`acr-password`** (required): Password for ACR authentication.
- **`github-token`** (required): GitHub token for authentication with `ghcr.io`.
- **`build-args`** (optional): Build arguments to pass to the Docker build.
- **`build-secrets`** (optional): Secrets to pass to the Docker build.
- **`actor`** (required): GitHub actor (username) for authentication.
- **`ssh_socket_forward`** (optional): Enables SSH socket forwarding. Defaults to `false`.
- **`context`** (optional): Build context for the Docker build. Defaults to `.`.

## Outputs

- **`tags`**: List of fully qualified image tags pushed to the ACR.

## Usage

```yaml
    - name: Build & push to ACR
      uses: dronetag/actions/build-push-acr@main
      with: 
      tags: "1.2.3"
      repository-name: "funnel"
      github-token: ${{ secrets.github-token }}
      acr-username: ${{ secrets.acr-username }}
      acr-password: ${{ secrets.acr-password }}
      actor: ${{ github.actor }}
      build-secrets: |
          "private_pip_url=https://${{ secrets.private-pypi-host }}"
          "private_pip_username=${{ secrets.private-pypi-user }}"
          "private_pip_password=${{ secrets.private-pypi-pass }}"
      ssh_socket_forward: "true"
```