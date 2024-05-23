#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#ifdef __unix__
#define API __attribute__((visibility("default")))
#else
#define API __declspec(dllexport) 
#endif

API void test()
{
    printf("Hello, world!\n");
}


struct initMapData 
{
    uint8_t r;
    uint8_t g;
    uint8_t b;
    uint8_t a;
    size_t length;
    uint32_t* map;
};
API uint8_t* initMap(struct initMapData* mapData)
{
    uint8_t* map = malloc(mapData->length);
    for(int i = 0; i < mapData->length; i+=4)
    {
        map[i+0] = mapData->a;
        map[i+1] = mapData->b;
        map[i+2] = mapData->g;
        map[i+3] = mapData->r;
    }

    return map;
}
