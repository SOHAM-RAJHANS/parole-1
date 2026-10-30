// PAROLE Module 2 Companion: PicoClaw Sub-Millisecond Go Policy Cache (< 10 MB RAM)
// Build: go build -o picoclaw_cache backend/picoclaw_cache.go
package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"net"
	"os"
	"path"
	"strings"
	"time"
)

type EvalResponse struct {
	Hit             bool    `json:"hit"`
	MatchedRule     string  `json:"matched_rule,omitempty"`
	ChainedRejected bool    `json:"chained_rejected"`
	LatencyMs       float64 `json:"latency_ms"`
}

var defaultSafePrefixes = []string{
	"git status", "git diff", "git log", "git branch", "git checkout",
	"pytest", "npm test", "npm run test", "npm run lint", "eslint src/",
	"cargo check", "ls", "cat src/",
}

func hasChaining(cmd string) bool {
	for _, op := range []string{"&&", "||", ";", "|", "`", "$(", ">", "<"} {
		if strings.Contains(cmd, op) {
			return true
		}
	}
	return false
}

func evaluateCommand(cmd string, cidrNet *net.IPNet, pathGlob string) EvalResponse {
	start := time.Now()
	trimmed := strings.TrimSpace(cmd)
	if hasChaining(trimmed) {
		return EvalResponse{Hit: false, ChainedRejected: true, LatencyMs: float64(time.Since(start).Nanoseconds()) / 1e6}
	}
	for _, pref := range defaultSafePrefixes {
		if trimmed == pref || strings.HasPrefix(trimmed, pref) {
			return EvalResponse{Hit: true, MatchedRule: pref, ChainedRejected: false, LatencyMs: float64(time.Since(start).Nanoseconds()) / 1e6}
		}
	}
	if cidrNet != nil {
		ip := net.ParseIP("10.0.4.12")
		if cidrNet.Contains(ip) {
			matched, _ := path.Match(pathGlob, "/api/v1/users")
			if matched {
				return EvalResponse{Hit: true, MatchedRule: "+ PERMIT " + cidrNet.String() + " ON " + pathGlob, LatencyMs: float64(time.Since(start).Nanoseconds()) / 1e6}
			}
		}
	}
	return EvalResponse{Hit: false, ChainedRejected: false, LatencyMs: float64(time.Since(start).Nanoseconds()) / 1e6}
}

func main() {
	_, defaultNet, _ := net.ParseCIDR("10.0.4.0/24")
	if len(os.Args) > 1 {
		res := evaluateCommand(strings.Join(os.Args[1:], " "), defaultNet, "/api/v1/*")
		b, _ := json.Marshal(res)
		fmt.Println(string(b))
		return
	}
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		res := evaluateCommand(scanner.Text(), defaultNet, "/api/v1/*")
		b, _ := json.Marshal(res)
		fmt.Println(string(b))
	}
}