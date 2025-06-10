# Test Image Parsing Methods

- 테스트 파일
  - ./files/test.pdf
  - 크기: 21,488 KB
  - 장 수: 560 

| 종류                                                   | 소요 시간       | 최대 메모리 사용량  |
|------------------------------------------------------|-------------|-------------|
| Pdf2ImageMemoryParser                                | -           | OOM 발생      |
| Pdf2ImageDiskParser                                  | 1039.86 sec | 1.7193 MB   |
| PyMuPDFImageParser                                   | 399.91 sec  | 1.7814 MB   |
| PdfplumberMemoryImageParser - chunk                  | 496.12 sec  | 57.5703 MB  |
| PdfplumberMemoryImageParser - one, save_image-thread | 559.28 sec  | 399.6844 MB |
| PdfplumberMemoryImageParser - one, save_image-naive  | 490.55 sec  | 53.6228 MB  |
| PdfplumberMemoryImageParser - one, sync for all      | 느림          | -           |
| PdfplumberDiskImageParser - save_image-thread        | 571.43 sec  | 7.5114 MB   |
| PdfplumberDiskImageParser - save_image-naive         | 521.86 sec  | 7.4759 MB   |
