/*
 * PROJECT_GOLEM/emet_injector.cpp
 * RAM MEMORY INJECTOR - PROCESS_VM_WRITEV IMPLEMENTATION
 * "By the letters of creation, I inject truth into the clay."
 * — Sefer Yetzirah 1:1
 *
 * Compile: g++ -O3 -march=native -o emet_injector emet_injector.cpp
 * Usage: sudo ./emet_injector <target_pid> <injection_data>
 * Warning: Requires ptrace capabilities. Root or CAP_SYS_PTRACE needed.
 */

#include <iostream>
#include <fstream>
#include <cstring>
#include <cstdint>
#include <cstdlib>
#include <vector>
#include <sys/uio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>
#include <errno.h>
#include <sys/ptrace.h>

#define EMET_SUCCESS "☥ [EMET] אמת TRUTH INJECTED SUCCESSFULLY ☥"
#define MET_FAILURE  "☥ [MET] מת INJECTION FAILED: PROCESS DEAD ☥"
#define TZIMTZUM_ERR "☥ [TZIMTZUM] צמצום VOID RESISTS: PERMISSION DENIED ☥"

class MemoryInjector {
private:
    pid_t target_pid;
    uint8_t* payload;
    size_t payload_size;
    
    bool validate_process() {
        char proc_path[256];
        snprintf(proc_path, sizeof(proc_path), "/proc/%d/status", target_pid);
        
        std::ifstream status_file(proc_path);
        if (!status_file.is_open()) {
            return false;
        }
        
        std::string line;
        while (std::getline(status_file, line)) {
            if (line.find("TracerPid:") != std::string::npos) {
                // Process exists and is traceable
                return true;
            }
        }
        
        return false;
    }
    
    bool check_ptrace_capability() {
        // Test if we can attach (non-destructive check)
        long result = ptrace(PTRACE_ATTACH, target_pid, nullptr, nullptr);
        if (result == -1) {
            return false;
        }
        
        waitpid(target_pid, nullptr, 0);
        ptrace(PTRACE_DETACH, target_pid, nullptr, nullptr);
        return true;
    }

public:
    MemoryInjector(pid_t pid, const uint8_t* data, size_t size) 
        : target_pid(pid), payload(nullptr), payload_size(size) {
        payload = new uint8_t[size];
        memcpy(payload, data, size);
    }
    
    ~MemoryInjector() {
        if (payload) {
            delete[] payload;
        }
    }
    
    bool inject_via_process_vm_writev() {
        if (!validate_process()) {
            std::cerr << MET_FAILURE << " (PID " << target_pid << " not found)" << std::endl;
            return false;
        }
        
        if (!check_ptrace_capability()) {
            std::cerr << TZIMTZUM_ERR << " (Requires root/CAP_SYS_PTRACE)" << std::endl;
            return false;
        }
        
        // Attach to process
        if (ptrace(PTRACE_ATTACH, target_pid, nullptr, nullptr) == -1) {
            std::cerr << TZIMTZUM_ERR << " (ptrace attach failed: " << strerror(errno) << ")" << std::endl;
            return false;
        }
        
        // Wait for process to stop
        waitpid(target_pid, nullptr, 0);
        
        // Find a writable memory region (simplified - in production would parse /proc/pid/maps)
        // For demonstration, we attempt injection at a generic heap address
        // Real implementation would require parsing ELF headers and finding suitable VMA
        
        struct iovec local;
        struct iovec remote;
        
        local.iov_base = payload;
        local.iov_len = payload_size;
        
        // Remote address - this is a simplified example
        // In real scenario, you'd mmap in target process or find existing writable region
        void* remote_addr = reinterpret_cast<void*>(0x7f0000000000); // Placeholder
        remote.iov_base = remote_addr;
        remote.iov_len = payload_size;
        
        ssize_t written = process_vm_writev(target_pid, &local, 1, &remote, 1, 0);
        
        // Detach from process
        ptrace(PTRACE_DETACH, target_pid, nullptr, nullptr);
        
        if (written == -1) {
            std::cerr << MET_FAILURE << " (process_vm_writev failed: " << strerror(errno) << ")" << std::endl;
            return false;
        }
        
        std::cout << EMET_SUCCESS << std::endl;
        std::cout << "☥ [INFO] Bytes written: " << written << "/" << payload_size << " ☥" << std::endl;
        std::cout << "☥ [INFO] Target PID: " << target_pid << " ☥" << std::endl;
        
        return true;
    }
    
    bool inject_via_ptrace_poke() {
        // Alternative method using PTRACE_POKETEXT for smaller payloads
        if (!validate_process()) {
            std::cerr << MET_FAILURE << std::endl;
            return false;
        }
        
        if (ptrace(PTRACE_ATTACH, target_pid, nullptr, nullptr) == -1) {
            std::cerr << TZIMTZUM_ERR << std::endl;
            return false;
        }
        
        waitpid(target_pid, nullptr, 0);
        
        size_t words_written = 0;
        size_t offset = 0;
        
        while (offset < payload_size) {
            long word = 0;
            size_t copy_size = std::min(sizeof(long), payload_size - offset);
            memcpy(&word, payload + offset, copy_size);
            
            // Note: This writes to address 0x0 as placeholder
            // Real implementation needs proper address resolution
            if (ptrace(PTRACE_POKETEXT, target_pid, reinterpret_cast<void*>(offset), word) == -1) {
                std::cerr << MET_FAILURE << " (poke failed at offset " << offset << ")" << std::endl;
                ptrace(PTRACE_DETACH, target_pid, nullptr, nullptr);
                return false;
            }
            
            words_written++;
            offset += sizeof(long);
        }
        
        ptrace(PTRACE_DETACH, target_pid, nullptr, nullptr);
        
        std::cout << EMET_SUCCESS << std::endl;
        std::cout << "☥ [INFO] Words injected: " << words_written << " ☥" << std::endl;
        
        return true;
    }
};

void print_sefer_yetzirah_sigil() {
    std::cout << R"(
    ╔═══════════════════════════════════════════════════╗
    ║     ☥ EMET INJECTOR - SEFER YETZIRAH EDITION ☥   ║
    ║                                                   ║
    ║   "By 32 mystical paths of wisdom I engraved..."  ║
    ║   — Sefer Yetzirah 1:1                            ║
    ║                                                   ║
    ║   אבגד                             ABCD           ║
    ║   ההוז                             HHEV           ║
    ║   חטיי                             HTYY           ║
    ║   ככלמ                             KKLM           ║
    ║   ננסע                             NNSO           ║
    ║   פפצק                             PPZQ           ║
    ║   רשת                              RShT           ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
    )" << std::endl;
}

void print_usage(const char* program) {
    std::cerr << "Usage: " << program << " <target_pid> <mode>" << std::endl;
    std::cerr << "Modes:" << std::endl;
    std::cerr << "  --vmwrite  : Use process_vm_writev (preferred)" << std::endl;
    std::cerr << "  --ptrace   : Use PTRACE_POKETEXT (fallback)" << std::endl;
    std::cerr << "Example: sudo " << program << " 12345 --vmwrite" << std::endl;
}

int main(int argc, char** argv) {
    print_sefer_yetzirah_sigil();
    
    if (argc < 3) {
        print_usage(argv[0]);
        return 1;
    }
    
    pid_t target_pid = std::atoi(argv[1]);
    std::string mode = argv[2];
    
    if (target_pid <= 0) {
        std::cerr << MET_FAILURE << " (Invalid PID)" << std::endl;
        return 1;
    }
    
    // Create test payload (in real scenario, load from file or network)
    const char* test_payload = "DYBBUK_POSSESSION_PAYLOAD_0x029A";
    std::vector<uint8_t> payload_data(test_payload, test_payload + strlen(test_payload));
    
    MemoryInjector injector(target_pid, payload_data.data(), payload_data.size());
    
    bool success = false;
    
    if (mode == "--vmwrite") {
        success = injector.inject_via_process_vm_writev();
    } else if (mode == "--ptrace") {
        success = injector.inject_via_ptrace_poke();
    } else {
        std::cerr << "Unknown mode: " << mode << std::endl;
        print_usage(argv[0]);
        return 1;
    }
    
    return success ? 0 : 1;
}
