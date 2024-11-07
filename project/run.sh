#!/bin/bash

ILIST=($(powershell -Command "Get-NetIPAddress -AddressFamily IPv4 | Select-Object -ExpandProperty IPAddress"))
MIN_PORT=60000
TEMP_FILES=()

echo "Starting listeners and senders..."

for i in "${!ILIST[@]}"; do
    SERVER_IP="${ILIST[i]}"
    PORT=$((MIN_PORT + i))
    
    # Запуск слушателя в фоновом режиме
    python3 main.py listener "$SERVER_IP" "$PORT" > "listener_$i.log" &
    LISTENER_PID=$!
    TEMP_FILES+=("listener_$i.log")
    echo "Started listener on $SERVER_IP:$PORT with PID $LISTENER_PID"
    
    # Запуск отправителя
    python3 main.py sender "$SERVER_IP" "$PORT" > "sender_$i.log"
    TEMP_FILES+=("sender_$i.log")
done

echo "Done. Press any key to exit."
read -n 1 -s

echo "Shutting down listeners..."

# Завершение слушателей
for pid in $(pgrep -f "main.py listener"); do
    echo "Killing listener with PID $pid"
    kill -9 $pid
done

# Удаление временных файлов
for temp_file in "${TEMP_FILES[@]}"; do
    echo "Removing file $temp_file"
    rm -f "$temp_file"
done

echo "Cleanup complete."
