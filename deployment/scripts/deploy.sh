set -e

echo "Starting deployment of Personal Finance Tracker..."

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Java 17 if not present
if ! java -version 2>&1 | grep -q "17"; then
    echo "Installing Java 17..."
    sudo apt install openjdk-17-jdk -y
fi

# Install PostgreSQL if not present
if ! which psql > /dev/null; then
    echo "Installing PostgreSQL..."
    sudo apt install postgresql postgresql-contrib -y
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
fi

# Create application directory
sudo mkdir -p /opt/finance-tracker
cd /opt/finance-tracker

# Download or copy application JAR
if [ -f "target/personal-finance-tracker-1.0.0.jar" ]; then
    sudo cp target/personal-finance-tracker-1.0.0.jar ./app.jar
else
    echo "JAR file not found. Please build the application first with 'mvn clean package'"
    exit 1
fi

