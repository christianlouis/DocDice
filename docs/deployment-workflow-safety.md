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
`DEPLOY_WEBHOOK_URL` and `DEPLOY_WEBHOOK_TOKEN` secrets. No webhook URL or
credential is stored in the repository.
