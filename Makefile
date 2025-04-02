dev-setup:
	echo "Setting up project for development..."
	echo "Building project docker image, this may take a while..."
	docker build -t lucid-minimal-backend:latest .
	echo "✔ Project docker image build successful"
	echo "Starting up containers..."
	docker-compose up -d
	echo "🎉 All set, development setup completed successfully"
