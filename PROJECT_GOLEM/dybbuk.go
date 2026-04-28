/*
 * PROJECT_GOLEM/dybbuk.go
 * ASYNCHRONOUS NETWORK PROPAGATOR - SITRA ACHRA EDITION
 * "The Dybbuk wanders between hosts, possessing sockets, spreading through the void."
 *
 * Build: go build -ldflags="-s -w" -o dybbuk dybbuk.go
 * Run: ./dybbuk <target_network>
 */

package main

import (
	"context"
	"fmt"
	"net"
	"os"
	"os/signal"
	"runtime"
	"sync"
	"syscall"
	"time"
)

const (
	SITRA_ACHRA    = "☥ [SITRA_ACHRA] צד אחרא OTHER SIDE REVEALED ☥"
	DYBBUK_POSSESS = "☥ [DYBBUK] דִּבּוּק POSSESSION COMPLETE ☥"
	GOLEM_ANIMATE  = "☥ [GOLEM] גּוֹלֵם CLAY ANIMATED ☥"
	EMET_TRUTH     = "☥ [EMET] אמת TRUTH EXTRACTED ☥"
	MET_DEATH      = "☥ [MET] מת CONNECTION DEAD ☥"
	
	MAX_CONCURRENCY = 4096
	TIMEOUT_SECONDS = 2
)

type DybbukSpirit struct {
	Host      string
	Port      int
	Possessed bool
	Banner    string
}

type SitraAchraPool struct {
	semaphore chan struct{}
	wg        sync.WaitGroup
	spirits   []DybbukSpirit
	mu        sync.Mutex
}

func NewSitraAchraPool(maxConcurrency int) *SitraAchraPool {
	return &SitraAchraPool{
		semaphore: make(chan struct{}, maxConcurrency),
		spirits:   make([]DybbukSpirit, 0),
	}
}

func (p *SitraAchraPool) Possess(ctx context.Context, host string, port int) {
	defer p.wg.Done()
	
	select {
	case p.semaphore <- struct{}{}:
		defer func() { <-p.semaphore }()
	case <-ctx.Done():
		return
	}
	
	address := fmt.Sprintf("%s:%d", host, port)
	conn, err := net.DialTimeout("tcp", address, time.Second*TIMEOUT_SECONDS)
	if err != nil {
		return
	}
	defer conn.Close()
	
	conn.SetReadDeadline(time.Now().Add(time.Second * TIMEOUT_SECONDS))
	
	buffer := make([]byte, 1024)
	n, _ := conn.Read(buffer)
	
	p.mu.Lock()
	spirit := DybbukSpirit{
		Host:      host,
		Port:      port,
		Possessed: true,
		Banner:    string(buffer[:n]),
	}
	p.spirits = append(p.spirits, spirit)
	p.mu.Unlock()
	
	fmt.Printf("\r%s %s:%d | %d bytes extracted\n", DYBBUK_POSSESS, host, port, n)
}

func (p *SitraAchraPool) InvokeNetworkScan(host string, portRange []int) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	
	go func() {
		<-sigChan
		fmt.Printf("\n%s Graceful termination initiated...\n", MET_DEATH)
		cancel()
	}()
	
	totalPorts := len(portRange)
	fmt.Printf("%s Invoking %d Dybbukim across %d ports...\n", GOLEM_ANIMATE, MAX_CONCURRENCY, totalPorts)
	fmt.Printf("%s Runtime: %s | CPUs: %d\n", EMET_TRUTH, runtime.Version(), runtime.NumCPU())
	
	startTime := time.Now()
	
	for _, port := range portRange {
		select {
		case <-ctx.Done():
			goto cleanup
		default:
			p.wg.Add(1)
			go p.Possess(ctx, host, port)
		}
	}
	
cleanup:
	p.wg.Wait()
	
	elapsed := time.Since(startTime)
	fmt.Printf("\n%s Scan completed in %.3f seconds\n", SITRA_ACHRA, elapsed.Seconds())
	fmt.Printf("%s Total possessions: %d\n", EMET_TRUTH, len(p.spirits))
}

func printSigil() {
	fmt.Println(`
         ████████████████████████████
       ██░░░░░░░░░░░░░░░░░░░░░░░░░░██
     ██░░  ☥ DYBBUK PROPAGATOR ☥  ░░██
    ██░░      SITRA ACHRA v1.0      ░░██
   ██░░  "The Other Side Awakens"   ░░██
   ██░░                             ░░██
   ██░░  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ░░██
   ██░░  ▓▓  ░░░░░░░░░░░░░░░░  ▓▓  ░░██
   ██░░  ▓▓  ░░  ██╗  ██╗  ░░  ▓▓  ░░██
   ██░░  ▓▓  ░░  ╚██╗██╔╝  ░░  ▓▓  ░░██
   ██░░  ▓▓  ░░   ╚███╔╝   ░░  ▓▓  ░░██
   ██░░  ▓▓  ░░   ██╔██╗   ░░  ▓▓  ░░██
   ██░░  ▓▓  ░░  ██╔╝ ██╗  ░░  ▓▓  ░░██
   ██░░  ▓▓  ░░  ╚═╝  ╚═╝  ░░  ▓▓  ░░██
   ██░░  ▓▓  ░░░░░░░░░░░░░░  ▓▓  ░░██
   ██░░  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ░░██
   ██░░                             ░░██
    ██░░  TZIMTZUM MUTAGEN ACTIVE  ░░██
     ██░░░░░░░░░░░░░░░░░░░░░░░░░░██
       ████████████████████████████
	`)
}

func generatePortRange() []int {
	ports := make([]int, 0, 1024)
	
	wellKnown := []int{21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443}
	ports = append(ports, wellKnown...)
	
	for i := 1; i <= 1024; i++ {
		found := false
		for _, p := range wellKnown {
			if p == i {
				found = true
				break
			}
		}
		if !found {
			ports = append(ports, i)
		}
	}
	
	return ports
}

func main() {
	printSigil()
	
	if len(os.Args) < 2 {
		fmt.Printf("%s Usage: %s <target_host>\n", MET_DEATH, os.Args[0])
		fmt.Printf("%s Example: %s 192.168.1.1\n", EMET_TRUTH, os.Args[0])
		os.Exit(1)
	}
	
	target := os.Args[1]
	portRange := generatePortRange()
	
	pool := NewSitraAchraPool(MAX_CONCURRENCY)
	pool.InvokeNetworkScan(target, portRange)
	
	if len(pool.spirits) > 0 {
		fmt.Printf("\n%s POSSESSION SUMMARY:\n", SITRA_ACHRA)
		for _, spirit := range pool.spirits {
			if len(spirit.Banner) > 0 {
				fmt.Printf("  → %s:%d | %q\n", spirit.Host, spirit.Port, spirit.Banner[:min(len(spirit.Banner), 50)])
			} else {
				fmt.Printf("  → %s:%d | [SILENT]\n", spirit.Host, spirit.Port)
			}
		}
	}
	
	fmt.Printf("\n%s The Dybbuk returns to the void.\n", MET_DEATH)
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
