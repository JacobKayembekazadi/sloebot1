#!/bin/bash

# SSL Certificate Generation Script for SloeLux Performance Bot
# For production, use Let's Encrypt or your certificate provider

DOMAIN=${1:-sloelux-perfbot.yourdomain.com}
COUNTRY="US"
STATE="California"
CITY="San Francisco"
ORGANIZATION="SloeLux"
UNIT="IT Department"

echo "🔐 Generating SSL certificates for: $DOMAIN"

# Create private key
openssl genrsa -out sloelux-perfbot.key 2048

# Create certificate signing request
openssl req -new -key sloelux-perfbot.key -out sloelux-perfbot.csr -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/OU=$UNIT/CN=$DOMAIN"

# Create self-signed certificate (valid for 365 days)
openssl x509 -req -days 365 -in sloelux-perfbot.csr -signkey sloelux-perfbot.key -out sloelux-perfbot.crt

# Set proper permissions
chmod 600 sloelux-perfbot.key
chmod 644 sloelux-perfbot.crt

echo "✅ SSL certificates generated:"
echo "   Certificate: sloelux-perfbot.crt"
echo "   Private Key: sloelux-perfbot.key"
echo ""
echo "⚠️  For production, replace with certificates from your CA or Let's Encrypt"
echo ""
echo "🔧 Let's Encrypt command:"
echo "   certbot certonly --standalone -d $DOMAIN" 