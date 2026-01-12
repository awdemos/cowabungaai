	@echo "Supabase build started"
	@mkdir -p .logs

build-supabase: local-registry docker-supabase
	@echo "Supabase build started"
	@mkdir -p .logs
	@$(MAKE) docker-supabase DOCKER_FLAGS="$(DOCKER_FLAGS) $(SILENT_DOCKER_FLAGS)" ZARF_FLAGS="--flavor upstream $(ZARF_FLAGS) $(SILENT_ZARF_FLAGS)" > .logs/build-supabase.log 2>&1
	@echo "Supabase build completed"

