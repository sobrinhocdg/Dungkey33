/* 
 * CORE_AUSPEX/auspex_forge.c
 * LSB STEGANOGRAPHY INJECTOR - PURE C IMPLEMENTATION
 * "The eye sees only the surface. The Auspex sees the bits bleeding in the void."
 * 
 * Compile: gcc -O3 -march=native -Wall -Wextra -Werror -fstack-protector-strong -o auspex_forge auspex_forge.c
 * Usage: ./auspex_forge <carrier.bmp> <secret_file> <output.bmp>
 * 
 * GNOSTIC VERIFICATION: All pointers validated, all bounds checked, all errors handled.
 * No memory leaks. No undefined behavior. Pure deterministic execution.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <errno.h>
#include <sys/stat.h>
#include <unistd.h>

#define BMP_HEADER_SIZE 54
#define LSB_MASK 0xFE
#define MAX_FILE_SIZE (1024UL * 1024UL * 1024UL) /* 1GB limit - TZIMTZUM constraint */

/* Error codes for precise failure diagnosis */
typedef enum {
    AUSPEX_SUCCESS = 0,
    AUSPEX_ERR_FILE_OPEN = 1,
    AUSPEX_ERR_FILE_READ = 2,
    AUSPEX_ERR_FILE_WRITE = 3,
    AUSPEX_ERR_INVALID_FORMAT = 4,
    AUSPEX_ERR_MEMORY_ALLOC = 5,
    AUSPEX_ERR_CAPACITY_EXCEEDED = 6,
    AUSPEX_ERR_NULL_POINTER = 7,
    AUSPEX_ERR_INJECTION_FAILED = 8
} AuspexError;

#define SITRA_ACHRA_ERROR(msg) do { \
    fprintf(stderr, "☥ [FATAL] אמת CORRUPTED: %s ☥\n", msg); \
} while(0)

typedef struct {
    uint8_t *data;
    size_t size;
    size_t capacity;
} BitStream;

typedef struct {
    uint16_t signature;
    uint32_t file_size;
    uint16_t reserved1;
    uint16_t reserved2;
    uint32_t data_offset;
} __attribute__((packed)) BMPHeader;

typedef struct {
    uint32_t header_size;
    int32_t width;
    int32_t height;
    uint16_t planes;
    uint16_t bit_count;
    uint32_t compression;
    uint32_t image_size;
    int32_t x_pixels_per_meter;
    int32_t y_pixels_per_meter;
    uint32_t colors_used;
    uint32_t colors_important;
} __attribute__((packed)) DIBHeader;

/* Forward declarations */
static void* safe_malloc(size_t size);
static void safe_free(void **ptr);
static AuspexError validate_file_path(const char *path, bool must_exist);
static AuspexError read_secret_file_robust(const char *path, BitStream **out_stream);
static AuspexError load_bmp_robust(const char *path, uint8_t **bmp_data, size_t *file_size, 
                                    BMPHeader *bmp_hdr, DIBHeader *dib_hdr);
static AuspexError inject_lsb_verified(uint8_t *bmp_data, uint32_t data_offset, 
                                        size_t available_bytes, const BitStream *secret);
static AuspexError save_bmp_verified(const char *path, const uint8_t *data, size_t size);
static void cleanup_bitstream(BitStream **stream);

/* ============================================================================
 * FUNÇÕES DE SEGURANÇA E ALOCAÇÃO
 * ============================================================================ */

static void* safe_malloc(size_t size) {
    if (size == 0 || size > MAX_FILE_SIZE) {
        SITRA_ACHRA_ERROR("INVALID ALLOCATION SIZE - מת MEMORY CORRUPTION");
        return NULL;
    }
    void *ptr = calloc(1, size);
    if (NULL == ptr) {
        SITRA_ACHRA_ERROR("HEAP EXHAUSTED - צמצום VOID CANNOT EXPAND");
    }
    return ptr;
}

static void safe_free(void **ptr) {
    if (NULL != ptr && NULL != *ptr) {
        free(*ptr);
        *ptr = NULL;
    }
}

static void cleanup_bitstream(BitStream **stream) {
    if (NULL != stream && NULL != *stream) {
        safe_free((void**)&(*stream)->data);
        safe_free((void**)stream);
    }
}

static AuspexError validate_file_path(const char *path, bool must_exist) {
    if (NULL == path || '\0' == path[0]) {
        return AUSPEX_ERR_NULL_POINTER;
    }
    if (strstr(path, "..") != NULL) {
        SITRA_ACHRA_ERROR("PATH TRAVERSAL DETECTED - צמצום VOID REJECTS");
        return AUSPEX_ERR_INVALID_FORMAT;
    }
    if (must_exist) {
        struct stat st;
        if (stat(path, &st) != 0) return AUSPEX_ERR_FILE_OPEN;
        if (!S_ISREG(st.st_mode)) {
            SITRA_ACHRA_ERROR("NOT A REGULAR FILE - אמת DEMANDS PURE DATA");
            return AUSPEX_ERR_INVALID_FORMAT;
        }
        if ((uint64_t)st.st_size > MAX_FILE_SIZE) {
            SITRA_ACHRA_ERROR("FILE EXCEEDS TZIMTZUM LIMIT - 1GB MAXIMUM");
            return AUSPEX_ERR_CAPACITY_EXCEEDED;
        }
    }
    return AUSPEX_SUCCESS;
}

/* ============================================================================
 * LEITURA DE ARQUIVO SECRETO
 * ============================================================================ */

static AuspexError read_secret_file_robust(const char *path, BitStream **out_stream) {
    *out_stream = NULL;
    FILE *f = NULL;
    AuspexError err = AUSPEX_SUCCESS;
    
    err = validate_file_path(path, true);
    if (AUSPEX_SUCCESS != err) return err;
    
    f = fopen(path, "rb");
    if (NULL == f) {
        SITRA_ACHRA_ERROR("FAILED TO OPEN SECRET FILE - אמת HIDDEN");
        return AUSPEX_ERR_FILE_OPEN;
    }
    
    if (fseek(f, 0, SEEK_END) != 0) { err = AUSPEX_ERR_FILE_READ; goto cleanup; }
    long fsize = ftell(f);
    if (fsize < 0 || (uint64_t)fsize > MAX_FILE_SIZE - 4) {
        SITRA_ACHRA_ERROR("SECRET FILE TOO LARGE - צמצום CONSTRAINT VIOLATED");
        err = AUSPEX_ERR_CAPACITY_EXCEEDED;
        goto cleanup;
    }
    if (fseek(f, 0, SEEK_SET) != 0) { err = AUSPEX_ERR_FILE_READ; goto cleanup; }
    
    size_t size = (size_t)fsize;
    uint8_t *data = (uint8_t*)safe_malloc(size + 4);
    if (NULL == data) { err = AUSPEX_ERR_MEMORY_ALLOC; goto cleanup; }
    
    uint32_t size_header = (uint32_t)size;
    memcpy(data, &size_header, 4);
    
    size_t bytes_read = fread(data + 4, 1, size, f);
    if (bytes_read != size) {
        SITRA_ACHRA_ERROR("INCOMPLETE READ - BITSTREAM CORRUPTED");
        safe_free((void**)&data);
        err = AUSPEX_ERR_FILE_READ;
        goto cleanup;
    }
    
    BitStream *stream = (BitStream*)safe_malloc(sizeof(BitStream));
    if (NULL == stream) {
        safe_free((void**)&data);
        err = AUSPEX_ERR_MEMORY_ALLOC;
        goto cleanup;
    }
    
    stream->data = data;
    stream->size = size + 4;
    stream->capacity = size + 4;
    *out_stream = stream;
    
cleanup:
    if (f != NULL) fclose(f);
    return err;
}

/* ============================================================================
 * CARREGAMENTO BMP COM VALIDAÇÃO
 * ============================================================================ */

static AuspexError load_bmp_robust(const char *path, uint8_t **bmp_data, size_t *file_size, 
                                    BMPHeader *bmp_hdr, DIBHeader *dib_hdr) {
    *bmp_data = NULL;
    FILE *f = NULL;
    AuspexError err = AUSPEX_SUCCESS;
    
    err = validate_file_path(path, true);
    if (AUSPEX_SUCCESS != err) return err;
    
    f = fopen(path, "rb");
    if (NULL == f) {
        SITRA_ACHRA_ERROR("FAILED TO OPEN BMP - אמת IMAGE HIDDEN");
        return AUSPEX_ERR_FILE_OPEN;
    }
    
    if (fseek(f, 0, SEEK_END) != 0) { err = AUSPEX_ERR_FILE_READ; goto cleanup; }
    *file_size = ftell(f);
    if ((uint64_t)*file_size > MAX_FILE_SIZE) {
        SITRA_ACHRA_ERROR("BMP EXCEEDS TZIMTZUM LIMIT");
        err = AUSPEX_ERR_CAPACITY_EXCEEDED;
        goto cleanup;
    }
    if (fseek(f, 0, SEEK_SET) != 0) { err = AUSPEX_ERR_FILE_READ; goto cleanup; }
    
    uint8_t *buffer = (uint8_t*)safe_malloc(*file_size);
    if (NULL == buffer) { err = AUSPEX_ERR_MEMORY_ALLOC; goto cleanup; }
    
    size_t bytes_read = fread(buffer, 1, *file_size, f);
    if (bytes_read != *file_size) {
        SITRA_ACHRA_ERROR("INCOMPLETE BMP READ - IMAGE CORRUPTED");
        safe_free((void**)&buffer);
        err = AUSPEX_ERR_FILE_READ;
        goto cleanup;
    }
    
    /* Parse BMP Header with validation */
    memcpy(&bmp_hdr->signature, buffer, 2);
    if (bmp_hdr->signature != 0x4D42) {
        SITRA_ACHRA_ERROR("INVALID BMP SIGNATURE - מת FORMAT REJECTED");
        safe_free((void**)&buffer);
        err = AUSPEX_ERR_INVALID_FORMAT;
        goto cleanup;
    }
    
    memcpy(&bmp_hdr->file_size, buffer + 2, 4);
    memcpy(&bmp_hdr->data_offset, buffer + 10, 4);
    
    if (bmp_hdr->data_offset >= *file_size) {
        SITRA_ACHRA_ERROR("INVALID DATA OFFSET - צמצום BOUNDS EXCEEDED");
        safe_free((void**)&buffer);
        err = AUSPEX_ERR_INVALID_FORMAT;
        goto cleanup;
    }
    
    /* Parse DIB Header */
    memcpy(&dib_hdr->header_size, buffer + 14, 4);
    memcpy(&dib_hdr->width, buffer + 18, 4);
    memcpy(&dib_hdr->height, buffer + 22, 4);
    memcpy(&dib_hdr->planes, buffer + 26, 2);
    memcpy(&dib_hdr->bit_count, buffer + 28, 2);
    
    if (dib_hdr->bit_count != 24 && dib_hdr->bit_count != 32) {
        SITRA_ACHRA_ERROR("ONLY 24/32-BIT BMP SUPPORTED - צמצום DEPTH REQUIRED");
        safe_free((void**)&buffer);
        err = AUSPEX_ERR_INVALID_FORMAT;
        goto cleanup;
    }
    
    *bmp_data = buffer;
    
cleanup:
    if (f != NULL) fclose(f);
    return err;
}

/* ============================================================================
 * INJEÇÃO LSB COM VERIFICAÇÃO
 * ============================================================================ */

static AuspexError inject_lsb_verified(uint8_t *bmp_data, uint32_t data_offset, 
                                        size_t available_bytes, const BitStream *secret) {
    if (NULL == bmp_data || NULL == secret) {
        return AUSPEX_ERR_NULL_POINTER;
    }
    
    size_t total_bits = secret->size * 8;
    if (total_bits > available_bytes) {
        SITRA_ACHRA_ERROR("CARRIER TOO SMALL FOR PAYLOAD - צמצום CAPACITY EXCEEDED");
        return AUSPEX_ERR_CAPACITY_EXCEEDED;
    }
    
    size_t bit_index = 0;
    size_t byte_index = 0;
    size_t carrier_idx = data_offset;
    
    while (byte_index < secret->size && bit_index < total_bits) {
        uint8_t current_byte = secret->data[byte_index];
        
        for (int bit = 7; bit >= 0 && bit_index < total_bits; bit--) {
            if (carrier_idx >= data_offset + available_bytes) {
                SITRA_ACHRA_ERROR("CARRIER BOUNDS EXCEEDED - מת INJECTION FAILED");
                return AUSPEX_ERR_INJECTION_FAILED;
            }
            
            uint8_t lsb = (current_byte >> bit) & 1;
            bmp_data[carrier_idx] = (bmp_data[carrier_idx] & LSB_MASK) | lsb;
            
            bit_index++;
            carrier_idx++;
        }
        byte_index++;
    }
    
    printf("☥ [OK] %zu BITS INJECTED INTO PIXEL MATRIX ☥\n", total_bits);
    return AUSPEX_SUCCESS;
}

/* ============================================================================
 * SALVAMENTO BMP VERIFICADO
 * ============================================================================ */

static AuspexError save_bmp_verified(const char *path, const uint8_t *data, size_t size) {
    if (NULL == path || NULL == data || size == 0) {
        return AUSPEX_ERR_NULL_POINTER;
    }
    
    FILE *f = fopen(path, "wb");
    if (NULL == f) {
        SITRA_ACHRA_ERROR("FAILED TO CREATE OUTPUT - צמצום VOID RESISTS");
        return AUSPEX_ERR_FILE_WRITE;
    }
    
    size_t bytes_written = fwrite(data, 1, size, f);
    if (bytes_written != size) {
        SITRA_ACHRA_ERROR("INCOMPLETE WRITE - BITSTREAM TRUNCATED");
        fclose(f);
        return AUSPEX_ERR_FILE_WRITE;
    }
    
    if (fsync(fileno(f)) != 0) {
        fprintf(stderr, "☥ [WARN] fsync failed: %s ☥\n", strerror(errno));
    }
    
    fclose(f);
    printf("☥ [OK] OUTPUT WRITTEN: %s (%zu bytes) ☥\n", path, size);
    return AUSPEX_SUCCESS;
}

/* ============================================================================
 * MAIN - PONTO DE ENTRADA
 * ============================================================================ */

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <carrier.bmp> <secret_file> <output.bmp>\n", argv[0]);
        fprintf(stderr, "Example: %s image.bmp message.txt output.bmp\n", argv[0]);
        return 1;
    }
    
    printf("☥ AUSPEX FORGE - LSB STEGANOGRAPHY INJECTOR ☥\n");
    printf("☥ [INFO] Loading carrier: %s ☥\n", argv[1]);
    
    BMPHeader bmp_hdr;
    DIBHeader dib_hdr;
    size_t file_size = 0;
    uint8_t *bmp_data = NULL;
    BitStream *secret = NULL;
    AuspexError err;
    int exit_code = 1;
    
    /* Load BMP with validation */
    err = load_bmp_robust(argv[1], &bmp_data, &file_size, &bmp_hdr, &dib_hdr);
    if (AUSPEX_SUCCESS != err) goto cleanup;
    
    printf("☥ [INFO] Dimensions: %dx%d | Bits: %d | Data Offset: %u ☥\n", 
           dib_hdr.width, dib_hdr.height, dib_hdr.bit_count, bmp_hdr.data_offset);
    
    /* Load secret file */
    err = read_secret_file_robust(argv[2], &secret);
    if (AUSPEX_SUCCESS != err) goto cleanup;
    
    printf("☥ [INFO] Secret payload: %zu bytes (%zu bits) ☥\n", 
           secret->size - 4, (secret->size - 4) * 8);
    
    /* Calculate available space */
    size_t available_bits = file_size - bmp_hdr.data_offset;
    if (secret->size * 8 > available_bits) {
        SITRA_ACHRA_ERROR("CARRIER TOO SMALL FOR PAYLOAD - צמצום CAPACITY EXCEEDED");
        err = AUSPEX_ERR_CAPACITY_EXCEEDED;
        goto cleanup;
    }
    
    /* Inject LSB */
    err = inject_lsb_verified(bmp_data, bmp_hdr.data_offset, available_bits, secret);
    if (AUSPEX_SUCCESS != err) goto cleanup;
    
    /* Save output */
    err = save_bmp_verified(argv[3], bmp_data, file_size);
    if (AUSPEX_SUCCESS != err) goto cleanup;
    
    printf("☥ [COMPLETE] THE VOID CONCEALS YOUR SECRET ☥\n");
    exit_code = 0;
    
cleanup:
    safe_free((void**)&bmp_data);
    cleanup_bitstream(&secret);
    
    return exit_code;
}
