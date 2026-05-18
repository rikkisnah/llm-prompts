<!-- #ai-assisted with OCA/OpenAI Model with human supervision -->

# Go Profile

Use Go modules.

Default targets:

- `setup`: `go mod download`.
- `format`: `gofmt -w`.
- `test`: `go test ./...`.
- `lint`: `go vet ./...` and `golangci-lint run` when available or required.

Strict mode should require `golangci-lint`.
