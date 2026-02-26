# Collect and filter proxy lists & save result
# 1. Copy required files from ../vpn-configs-for-russia
# 2. from each file remove the following lines with these substrings:
#   - security=none
#   - Russia
# 3. Destination: WHITE_LIST_PROXY_COLLECTION.txt

# Update the source locally
echo "Checking updates"
cd ../vpn-configs-for-russia/
git pull

# Copy required files
cd -
mkdir -p input/

cp ../vpn-configs-for-russia/WHITE-CIDR-RU-checked.txt input/
cp ../vpn-configs-for-russia/WHITE-SNI-RU-all.txt input/
cp ../vpn-configs-for-russia/Vless-Reality-White-Lists-Rus-Mobile.txt input/
cp ../vpn-configs-for-russia/Vless-Reality-White-Lists-Rus-Mobile-2.txt input/

# Clear output file if it exists
> WHITE_LIST_PROXY_COLLECTION.txt

# Process each file and filter content
for file in input/*.txt; do
    echo "Processing $file..."
    awk '
    /Russia/ { next }                                          # Skip lines with Russia (Our Primary Goal!)
    /type=tcp/ && /sec(urity|ure)=none/ { next }               # Skip type=tcp + security=none (VULNERABLE), order-agnostic
    /sec(urity|ure)=none/ && !/type=xhttp/ { next }            # Skip secure=none without type=xhttp
    { print }                                                  # Output valid lines
    ' "$file" >> WHITE_LIST_PROXY_COLLECTION.txt
done

echo "Done! Results saved to WHITE_LIST_PROXY_COLLECTION.txt"