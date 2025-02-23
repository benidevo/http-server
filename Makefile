start:
	./your_program.sh

test:
	codecrafters test

lint:
	isort ./app && black ./app
