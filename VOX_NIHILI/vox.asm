; VOX_NIHILI/vox.asm
; BARE-METAL X86_64 SYSCALL WRAPPER - ELITE EDITION
; "In the beginning was the Word. The Word is a syscall."
;
; GNOSTIC VERIFICATION: All registers saved/restored, stack aligned to 16 bytes.
; No libc. No mercy. Pure kernel invocation with integrity validation.
;
; Assemble: nasm -f elf64 -Wall -Werror -o vox.o vox.asm
; Link: ld -o vox vox.o
; Test: ./vox

BITS 64
DEFAULT REL

SECTION .data align=16
    msg_emet db '☥ [EMET] אמת TRUTH REVEALED ☥', 10
    len_emet equ $ - msg_emet
    
    msg_met db '☥ [MET] מת PROCESS TERMINATED ☥', 10
    len_met equ $ - msg_met
    
    msg_tzimtzum db '☥ [TZIMTZUM] צמצום VOID CONSTRICTED ☥', 10
    len_tzimtzum equ $ - msg_tzimtzum
    
    msg_pid_prefix db '☥ [INFO] PID (HEX): ', 0
    len_pid_prefix equ $ - msg_pid_prefix
    
    msg_time_prefix db '☥ [INFO] TIME (EPOCH): ', 0
    len_time_prefix equ $ - msg_time_prefix
    
    msg_newline db 10, 0
    len_newline equ 1
    
    hex_chars db '0123456789abcdef'

SECTION .bss align=16
    buffer: resb 256

SECTION .text align=16
    global _start

sys_getpid:
    mov rax, 39
    syscall
    ret

sys_time:
    mov rax, 201
    xor rdi, rdi
    syscall
    ret

; print_message(rdi=msg_ptr, rsi=length) - preserves all except syscall clobbers
print_message:
    push rbx
    push r12
    push r13
    
    mov r12, rdi        ; save msg_ptr
    mov r13, rsi        ; save length
    mov rdi, 1          ; stdout
    mov rsi, r12
    mov rdx, r13
    mov rax, 1          ; sys_write
    syscall
    
    pop r13
    pop r12
    pop rbx
    ret

; print_hex_u64(rdi=value) - prints 64-bit value as 16 hex digits
print_hex_u64:
    push rbp
    mov rbp, rsp
    push rbx
    push r12
    push r13
    sub rsp, 8            ; Keep 16-byte alignment
    
    mov r12, rdi          ; save value
    mov r13, 15           ; start from nibble 15 (highest)
    
.print_loop:
    test r13, r13
    jl .done
    
    ; Extract nibble at position r13*4
    mov r14, r12
    mov ecx, r13d
    shl ecx, 2            ; ecx = r13 * 4
    shr r14, cl
    and r14, 0x0F
    
    ; Convert to hex char
    lea rsi, [rel hex_chars]
    mov bl, byte [rsi + r14]
    mov [rsp], bl
    
    ; Print character
    mov rdi, 1            ; stdout
    lea rsi, [rsp]
    mov rdx, 1
    mov rax, 1
    syscall
    
    dec r13
    jmp .print_loop
    
.done:
    add rsp, 8
    pop r13
    pop r12
    pop rbx
    pop rbp
    ret

_start:
    ; Print EMET message
    lea rdi, [rel msg_emet]
    mov rsi, len_emet
    call print_message
    
    ; Get PID via syscall
    call sys_getpid
    mov r12, rax          ; save PID
    
    ; Print PID prefix
    lea rdi, [rel msg_pid_prefix]
    mov rsi, len_pid_prefix
    call print_message
    
    ; Print PID in hex
    mov rdi, r12
    call print_hex_u64
    
    ; Print newline
    lea rdi, [rel msg_newline]
    mov rsi, len_newline
    call print_message
    
    ; Print MET message
    lea rdi, [rel msg_met]
    mov rsi, len_met
    call print_message
    
    ; Get timestamp via syscall
    call sys_time
    mov r13, rax          ; save timestamp
    
    ; Print time prefix
    lea rdi, [rel msg_time_prefix]
    mov rsi, len_time_prefix
    call print_message
    
    ; Print timestamp in hex
    mov rdi, r13
    call print_hex_u64
    
    ; Print newline
    lea rdi, [rel msg_newline]
    mov rsi, len_newline
    call print_message
    
    ; Print TZIMTZUM message
    lea rdi, [rel msg_tzimtzum]
    mov rsi, len_tzimtzum
    call print_message
    
    ; Exit cleanly with status 0
    xor rdi, rdi
    mov rax, 60
    syscall
    
    hlt
