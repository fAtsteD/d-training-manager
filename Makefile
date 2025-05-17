build-DTrainingManagerFunction:
	mkdir -p $(ARTIFACTS_DIR)/d_training_manager
	cd src/d_training_manager && find . -type f -name '*.py' -exec cp --parents {} $(ARTIFACTS_DIR)/d_training_manager \; && cd - > /dev/null
	cp requirements.txt $(ARTIFACTS_DIR)
	python -m pip install -r requirements.txt -t $(ARTIFACTS_DIR)
	rm -rf $(ARTIFACTS_DIR)/bin
