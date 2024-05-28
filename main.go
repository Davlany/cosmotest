package main

import (
	"fmt"
	"log"
	"regexp"
	"strings"
	"time"

	expect "github.com/google/goexpect"
)

func extractConnection(output string) string {
	// Регулярное выражение для поиска строки Connection
	re := regexp.MustCompile(`(?m)^\s*\d+\s+\w+\s+\w+/\w+\s+([\w/]+)/[\w/]+\s+\w+$`)
	matches := re.FindStringSubmatch(output)

	if len(matches) > 1 {
		return matches[1]
	}
	return ""
}

func main() {
	// Конфигурация для Telnet
	host := "10.6.50.38"
	// port := "23"
	username := "smile"
	password := "xibypew"
	command := "show ports 1"

	// Создание Telnet-сессии
	exp, _, err := expect.Spawn(fmt.Sprintf("telnet %s", host), -1)
	log.Print("Connecting")
	if err != nil {
		log.Fatalf("Failed to start telnet session: %v", err)
	}
	defer exp.Close()

	log.Print("Login")
	_, err = exp.ExpectBatch([]expect.Batcher{
		&expect.BExp{R: "UserName:"},
		&expect.BSnd{S: username + "\n"},
		&expect.BExp{R: "Password:"},
		&expect.BSnd{S: password + "\n"},
		&expect.BExp{R: "#"}, // ожидаем приглашение командной строки
	}, 10*time.Second)
	if err != nil {
		log.Fatalf("Failed to login: %v", err)
	}
	log.Print("Command")
	// Выполнение команды
	err = exp.Send(command + "\n")
	if err != nil {
		log.Fatalf("Failed to send command: %v", err)
	}

	// Ожидание и вывод результата команды
	result, err := exp.ExpectBatch([]expect.Batcher{
		&expect.BExp{R: "#"}, // ожидаем приглашение командной строки после выполнения команды
	}, 20*time.Second)
	if err != nil {
		log.Fatalf("Failed to get command output: %v", err)
	}

	// Печать результата
	fmt.Println(result[0].Output)
	output := strings.TrimSpace(result[0].Output)
	fmt.Println(output)
	connections := extractConnection(output)
	if connections == "" {
		log.Println("Failed to extract connection")
	} else {
		fmt.Println("Connection:", connections)
	}

	// Завершение сессии
	err = exp.Send("exit\n")
	if err != nil {
		log.Fatalf("Failed to exit: %v", err)
	}
}
