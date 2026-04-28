/*
 * OUROBOROS/tzimtzum_mutagen.c
 * POLYMORPHIC/METAMORPHIC CODE ENGINE
 * "The void contracts to make space for creation. The code mutates to evade detection."
 *
 * Compile: gcc -O3 -march=native -fno-stack-protector -z execstack -o tzimtzum_mutagen tzimtzum_mutagen.c
 * Run: ./tzimtzum_mutagen
 *
 * WARNING: This is a demonstration of self-modifying code concepts.
 * The mutation happens in RAM, rewriting ADD to SUB instructions dynamically.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/mman.h>
#include <signal.h>
#include <time.h>

#define TZIMTZUM_CONTRACT "☥ [TZIMTZUM] צמצום VOID CONTRACTING... ☥"
#define MUTAGEN_SHIFT     "☥ [MUTAGEN] BINAY SHIFT DETECTED ☥"
#define OUROBOROS_CYCLE   "☥ [OUROBOROS] THE SNAKE CONSUMES ITSELF ☥"
#define EMET_VERIFICATION "☥ [EMET] אמת INTEGRITY VERIFIED ☥"
#define MET_CORRUPTION    "☥ [MET] מת CODE CORRUPTED ☥"

// Mutation opcodes (x86_64)
#define OP_ADD 0x01      // add %al, (%rax)
#define OP_SUB 0x28      // sub %al, (%rax)  
#define OP_NOP 0x90      // nop
#define OP_JMP 0xEB      // jmp short

typedef struct {
    uint8_t* code_ptr;
    size_t code_size;
    uint32_t generation;
    uint8_t checksum;
} MutagenContext;

// Shellcode template - simple computation that can be mutated
// Original: ADD operations
static uint8_t shellcode_template[] = {
    0x48, 0xc7, 0xc0, 0x0a, 0x00, 0x00, 0x00,  // mov $0xa, %rax
    0x48, 0x89, 0xc1,                          // mov %rax, %rcx
    0x04, 0x05,                                // add $0x5, %al
    0x04, 0x03,                                // add $0x3, %al
    0x04, 0x02,                                // add $0x2, %al
    0xc3                                       // ret
};

static uint8_t compute_checksum(uint8_t* data, size_t len) {
    uint8_t sum = 0;
    for (size_t i = 0; i < len; i++) {
        sum ^= data[i];
    }
    return sum;
}

static void print_hex_dump(const char* label, uint8_t* data, size_t len) {
    printf("%s", label);
    for (size_t i = 0; i < len && i < 32; i++) {
        printf("%02X ", data[i]);
    }
    printf("\n");
}

static int make_writable(void* addr, size_t len) {
    long pagesize = sysconf(_SC_PAGESIZE);
    void* aligned_addr = (void*)((uintptr_t)addr & ~(pagesize - 1));
    
    if (mprotect(aligned_addr, len + (uintptr_t)addr - (uintptr_t)aligned_addr, 
                 PROT_READ | PROT_WRITE | PROT_EXEC) == -1) {
        perror("mprotect");
        return -1;
    }
    return 0;
}

static MutagenContext* create_mutagen() {
    MutagenContext* ctx = malloc(sizeof(MutagenContext));
    if (!ctx) return NULL;
    
    ctx->code_size = sizeof(shellcode_template);
    ctx->code_ptr = malloc(ctx->code_size);
    if (!ctx->code_ptr) {
        free(ctx);
        return NULL;
    }
    
    memcpy(ctx->code_ptr, shellcode_template, ctx->code_size);
    ctx->generation = 0;
    ctx->checksum = compute_checksum(ctx->code_ptr, ctx->code_size);
    
    return ctx;
}

static void mutate_add_to_sub(MutagenContext* ctx) {
    // Find ADD instructions and convert to SUB
    // This is a simplified demonstration - real polymorphic engines are more complex
    
    for (size_t i = 0; i < ctx->code_size - 1; i++) {
        if (ctx->code_ptr[i] == 0x04) {  // add imm8, %al
            // Mutate ADD to SUB by changing opcode
            ctx->code_ptr[i] = 0x2c;  // sub imm8, %al
            printf("%s Byte %zu: ADD(0x04) → SUB(0x2c)\n", MUTAGEN_SHIFT, i);
        }
    }
    
    ctx->generation++;
    ctx->checksum = compute_checksum(ctx->code_ptr, ctx->code_size);
}

static void mutate_sub_to_add(MutagenContext* ctx) {
    // Reverse mutation: SUB back to ADD
    for (size_t i = 0; i < ctx->code_size - 1; i++) {
        if (ctx->code_ptr[i] == 0x2c) {  // sub imm8, %al
            ctx->code_ptr[i] = 0x04;  // add imm8, %al
            printf("%s Byte %zu: SUB(0x2c) → ADD(0x04)\n", MUTAGEN_SHIFT, i);
        }
    }
    
    ctx->generation++;
    ctx->checksum = compute_checksum(ctx->code_ptr, ctx->code_size);
}

static void inject_noise(MutagenContext* ctx) {
    // Insert NOP sleds as camouflage
    if (ctx->code_size + 4 < 256) {
        uint8_t* new_code = realloc(ctx->code_ptr, ctx->code_size + 4);
        if (new_code) {
            ctx->code_ptr = new_code;
            memmove(ctx->code_ptr + 4, ctx->code_ptr, ctx->code_size);
            ctx->code_ptr[0] = OP_NOP;
            ctx->code_ptr[1] = OP_NOP;
            ctx->code_ptr[2] = OP_NOP;
            ctx->code_ptr[3] = OP_NOP;
            ctx->code_size += 4;
            ctx->checksum = compute_checksum(ctx->code_ptr, ctx->code_size);
            printf("%s Injected 4-byte NOP sled\n", OUROBOROS_CYCLE);
        }
    }
}

static void verify_integrity(MutagenContext* ctx) {
    uint8_t current_sum = compute_checksum(ctx->code_ptr, ctx->code_size);
    if (current_sum == ctx->checksum) {
        printf("%s Generation %u checksum: 0x%02X\n", 
               EMET_VERIFICATION, ctx->generation, current_sum);
    } else {
        printf("%s Checksum mismatch! Expected 0x%02X, got 0x%02X\n",
               MET_CORRUPTION, ctx->checksum, current_sum);
    }
}

static void execute_shellcode(MutagenContext* ctx) {
    // Make code executable
    if (make_writable(ctx->code_ptr, ctx->code_size) == -1) {
        printf("%s Failed to make memory executable\n", MET_CORRUPTION);
        return;
    }
    
    typedef int (*shellcode_func)(void);
    shellcode_func func = (shellcode_func)ctx->code_ptr;
    
    int result = func();
    printf("☥ [EXEC] Shellcode returned: %d ☥\n", result);
}

static void print_ouroboros_sigil(uint32_t generation) {
    printf(R"(
         ╔═══════════════════════════════════════╗
         ║    ☥ TZIMTZUM MUTAGEN ENGINE ☥       ║
         ║                                       ║
         ║      ████████████████████████         ║
         ║    ██░░░░░░░░░░░░░░░░░░░░░░██         ║
         ║   ██░░  OUROBOROS CYCLE   ░░██        ║
         ║  ██░░   GENESIS → APOCALYPSE ░░██     ║
         ║  ██░░                         ░░██     ║
         ║  ██░░  ▄▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▄  ░░██     ║
         ║  ██░░ █  GENERATION: %-3u   █ ░░██     ║
         ║  ██░░  ▀▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▀  ░░██     ║
         ║  ██░░                         ░░██     ║
         ║   ██░░  SELF-MODIFYING CODE  ░░██      ║
         ║    ██░░░░░░░░░░░░░░░░░░░░░░██         ║
         ║      ████████████████████████         ║
         ║                                       ║
         ╚═══════════════════════════════════════╝
    )", generation);
}

static void cleanup_mutagen(MutagenContext* ctx) {
    if (ctx) {
        if (ctx->code_ptr) {
            free(ctx->code_ptr);
        }
        free(ctx);
    }
}

int main(int argc, char** argv) {
    printf(TZIMTZUM_CONTRACT "\n");
    printf(OUROBOROS_CYCLE "\n\n");
    
    MutagenContext* ctx = create_mutagen();
    if (!ctx) {
        fprintf(stderr, "Failed to create mutagen context\n");
        return 1;
    }
    
    print_ouroboros_sigil(ctx->generation);
    
    printf("\n--- INITIAL STATE ---\n");
    print_hex_dump("Original: ", ctx->code_ptr, ctx->code_size);
    verify_integrity(ctx);
    
    printf("\n--- MUTATION CYCLE 1: ADD → SUB ---\n");
    mutate_add_to_sub(ctx);
    print_hex_dump("Mutated:  ", ctx->code_ptr, ctx->code_size);
    verify_integrity(ctx);
    
    printf("\n--- MUTATION CYCLE 2: NOISE INJECTION ---\n");
    inject_noise(ctx);
    print_hex_dump("Camouflaged: ", ctx->code_ptr, ctx->code_size);
    verify_integrity(ctx);
    
    printf("\n--- MUTATION CYCLE 3: SUB → ADD (REVERSION) ---\n");
    mutate_sub_to_add(ctx);
    print_hex_dump("Reverted: ", ctx->code_ptr, ctx->code_size);
    verify_integrity(ctx);
    
    printf("\n--- EXECUTION TEST ---\n");
    execute_shellcode(ctx);
    
    printf("\n" OUROBOROS_CYCLE "\n");
    printf("Final Generation: %u\n", ctx->generation);
    printf("Final Checksum: 0x%02X\n", ctx->checksum);
    
    cleanup_mutagen(ctx);
    
    printf("\n☥ [COMPLETE] THE SNAKE RETURNS TO THE VOID ☥\n");
    return 0;
}
