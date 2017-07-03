#include <cstdlib>
#include <iostream>
#include <ctime>

using namespace std;



uint8_t distanceWegner(uint8_t val) {
  uint8_t dist = 0;
  while (val != 0) {
        // A bit is set, so increment the count and clear the bit
        ++dist;
        val &= val - 1;
    }
  return dist;  
}

uint8_t distancePopcount(uint8_t val) {
  return __builtin_popcount(val);
}

uint32_t distanceWegner(uint32_t val) {
  uint32_t dist = 0;
  while (val != 0) {
        // A bit is set, so increment the count and clear the bit
        ++dist;
        val &= val - 1;
    }
  return dist;  
}

uint8_t lookUpTbl[256];
void initLookUpTbl() {
  for (int i=0; i<256; i++) {
    lookUpTbl[i] = distancePopcount(i);
  }
}

uint8_t performLookUp(int val) {
  return lookUpTbl[val];
}

uint32_t distancePopcount(uint32_t num) {
  return __builtin_popcount(num);
}

uint64_t distanceWegner(uint64_t num) {
  uint64_t dist = 0;
  while (num != 0) {
        // A bit is set, so increment the count and clear the bit
        ++dist;
        num &= num - 1;
    }
  return dist;  
}

uint64_t distancePopcount(uint64_t num) {
  return __builtin_popcount(num);
}

int main(int argc, char *argv[]) {
  uint arrSize = 10000000;
  uint8_t* random8BitInts = new uint8_t[arrSize];
  uint32_t* random32BitInts = new uint32_t[arrSize];
  uint64_t* random64BitInts = new uint64_t[arrSize];
  initLookUpTbl();

  for(int i=0; i<arrSize; i++) {
    random8BitInts[i] = rand() % 255; //random number [1,255]
    random32BitInts[i] = rand() % 4294967296; //random number [1, 2^32]
    random64BitInts[i] = rand() % 18446744073709551615ull; //random number [1, 2^64]
  }
  //also check to verify that popcount returns the correct thing
 
  clock_t begin_map_8 = clock();
  for(int i=0; i<arrSize; i++) {
    performLookUp(random8BitInts[i]);
  }
  clock_t end_map_8 = clock();

  clock_t begin_wegner_8 = clock();
  for(int i=0; i<arrSize; i++) {
    distanceWegner(random8BitInts[i]);
  }
  clock_t end_wegner_8 = clock();

  clock_t begin_popcount_8 = clock();
  for(int i=0; i<arrSize; i++) {
    distancePopcount(random8BitInts[i]);
  }
  clock_t end_popcount_8 = clock();
  
  clock_t begin_map_32 = clock();
  /*  for(int i=0; i<arrSize; i++) {
    performLookUp(random32BitInts[i] >> 24) + \
      performLookUp(random32BitInts[i] >> 16 & 0xFF) + \
      performLookUp(random32BitInts[i] >> 8 & 0xFF) + \
      performLookUp(random32BitInts[i] & 0xFF);
      }*/
  for(int i=0; i<arrSize; i++) {
    uint8_t *ptr = (uint8_t *)&random32BitInts[i];
    performLookUp(*ptr++) +
    performLookUp(*ptr++) +
    performLookUp(*ptr++) +
    performLookUp(*ptr);
  }

  clock_t end_map_32 = clock();

  clock_t begin_wegner_32 = clock();
  for(int i=0; i<arrSize; i++) {
    distanceWegner(random32BitInts[i]);
  }
  clock_t end_wegner_32 = clock();
  
  clock_t begin_popcount_32 = clock();
  for(int i=0; i<arrSize; i++) {
    distancePopcount(random32BitInts[i]);
  }
  clock_t end_popcount_32 = clock();
  
  clock_t begin_wegner_64 = clock();
  for(int i=0; i<arrSize; i++) {
    distanceWegner(random64BitInts[i]);
  }
  clock_t end_wegner_64 = clock();

  clock_t begin_popcount_64 = clock();
  for(int i=0; i<arrSize; i++) {
    distancePopcount(random64BitInts[i]);
  }
  clock_t end_popcount_64 = clock();
  cout << "8 bit map: " << end_map_8 - begin_map_8 << endl;
  cout << "8 bit wegner: " << end_wegner_8 - begin_wegner_8 << endl;
  cout << "8 bit popcount: " << end_popcount_8 - begin_popcount_8 << endl;
  cout << "32 bit map: " << end_map_32 - begin_map_32 << endl;
  cout << "32 bit wegner: " << end_wegner_32 - begin_wegner_32 << endl;
  cout << "32 bit popcount: " << end_popcount_32 - begin_popcount_32 << endl;
  cout << "64 bit wegner: " << end_wegner_64 - begin_wegner_64 << endl;
  cout << "64 bit popcount: " << end_popcount_64 - begin_popcount_64 << endl;


  delete[] random8BitInts;
  delete[] random32BitInts;
  delete[] random64BitInts;
}
