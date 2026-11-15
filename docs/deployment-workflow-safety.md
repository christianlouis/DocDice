# Deployment workflow safety

The former container workflow ran with `push: true` on pull requests and was
named `Build and Push Docker Image`. A `workflow_run` deploy workflow matched
that name without checking the event conclusion, so a pull-request build could
trigger a production webhook. The container workflow is now named
`Build and Publish Container`, builds pull requests without registry login or
push, and publishes only branch pushes. The `latest` tag is emitted only for
`main`; `develop` receives a commit tag.

Production deployment is now exclusively a manual `workflow_dispatch` on the
`main` branch and requires the `production` environment plus
the `DEPLOY_WEBHOOK_URL` secret. The workflow preserves the existing webhook
contract: it sends only a POST request, without invented headers or a JSON
body. Configure that secret in the production environment; no URL or
credential is stored in the repository, and no secret rotation is performed by
this change.
