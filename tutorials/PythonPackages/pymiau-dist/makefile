clean:
	@find . -name '*~' -delete
	@find . -name '__pycache__' -type d | xargs rm -fr
	@find . -name '*.egg-info' -type d | xargs rm -fr

cleandist:
	@rm -rf dist/*.*

cleanall:clean cleandist

