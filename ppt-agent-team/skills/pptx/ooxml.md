# Office Open XML (OOXML) 기술 참조

PowerPoint 파일의 XML 레벨 편집을 위한 기술 문서입니다.

## PPTX 파일 구조

PPTX 파일은 ZIP 압축된 XML 파일들의 집합입니다.

```
presentation.pptx (압축 해제 후)
│
├── [Content_Types].xml          # 콘텐츠 타입 선언
├── _rels/
│   └── .rels                    # 최상위 관계 정의
│
├── docProps/
│   ├── app.xml                  # 앱 속성 (슬라이드 수 등)
│   ├── core.xml                 # 코어 속성 (제목, 작성자)
│   └── thumbnail.jpeg           # 썸네일 이미지
│
└── ppt/
    ├── presentation.xml         # 메인 프리젠테이션 파일
    ├── presProps.xml            # 프리젠테이션 속성
    ├── tableStyles.xml          # 테이블 스타일
    ├── viewProps.xml            # 뷰 속성
    │
    ├── _rels/
    │   └── presentation.xml.rels  # 프리젠테이션 관계
    │
    ├── slides/
    │   ├── slide1.xml           # 슬라이드 1
    │   ├── slide2.xml           # 슬라이드 2
    │   └── _rels/
    │       ├── slide1.xml.rels  # 슬라이드 1 관계
    │       └── slide2.xml.rels  # 슬라이드 2 관계
    │
    ├── slideLayouts/
    │   ├── slideLayout1.xml     # 타이틀 레이아웃
    │   ├── slideLayout2.xml     # 타이틀+콘텐츠
    │   └── ...
    │
    ├── slideMasters/
    │   └── slideMaster1.xml     # 마스터 슬라이드
    │
    ├── theme/
    │   └── theme1.xml           # 테마 정의 (색상, 폰트)
    │
    ├── noteSlides/
    │   └── notesSlide1.xml      # 발표자 노트
    │
    └── media/
        ├── image1.png           # 이미지 파일들
        └── image2.jpg
```

## XML 네임스페이스

```xml
xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
```

## 슬라이드 XML 구조

### 기본 슬라이드

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="..." xmlns:r="..." xmlns:p="...">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr/>

      <!-- 여기에 도형들 추가 -->

    </p:spTree>
  </p:cSld>
</p:sld>
```

### 텍스트 상자

```xml
<p:sp>
  <p:nvSpPr>
    <p:cNvPr id="2" name="TextBox 1"/>
    <p:cNvSpPr txBox="1"/>
    <p:nvPr/>
  </p:nvSpPr>

  <p:spPr>
    <a:xfrm>
      <a:off x="914400" y="914400"/>  <!-- 위치 (EMU) -->
      <a:ext cx="7315200" cy="914400"/> <!-- 크기 (EMU) -->
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>

  <p:txBody>
    <a:bodyPr/>
    <a:lstStyle/>
    <a:p>
      <a:r>
        <a:rPr lang="ko-KR" sz="2400" b="1">
          <a:solidFill>
            <a:srgbClr val="1A1A2E"/>
          </a:solidFill>
          <a:latin typeface="Arial"/>
        </a:rPr>
        <a:t>텍스트 내용</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
```

### 텍스트 포맷팅 속성

| 속성 | 설명 | 예시 |
|------|------|------|
| `sz` | 폰트 크기 (1/100 pt) | `sz="2400"` = 24pt |
| `b` | 굵게 | `b="1"` |
| `i` | 기울임 | `i="1"` |
| `u` | 밑줄 | `u="sng"` |
| `strike` | 취소선 | `strike="sngStrike"` |

### 색상 지정

```xml
<!-- RGB 색상 -->
<a:solidFill>
  <a:srgbClr val="E94560"/>
</a:solidFill>

<!-- 테마 색상 -->
<a:solidFill>
  <a:schemeClr val="accent1"/>
</a:solidFill>

<!-- 투명도 포함 -->
<a:solidFill>
  <a:srgbClr val="000000">
    <a:alpha val="50000"/>  <!-- 50% 불투명 -->
  </a:srgbClr>
</a:solidFill>
```

## 단위 시스템 (EMU)

PowerPoint는 EMU(English Metric Units)를 사용합니다.

```
1 인치 = 914400 EMU
1 포인트 = 12700 EMU
1 cm = 360000 EMU
```

### 변환 공식

```javascript
const emuPerInch = 914400;
const emuPerPt = 12700;
const emuPerCm = 360000;

function inchToEmu(inches) {
  return Math.round(inches * emuPerInch);
}

function ptToEmu(points) {
  return Math.round(points * emuPerPt);
}

function cmToEmu(cm) {
  return Math.round(cm * emuPerCm);
}
```

## 이미지 추가

### 1. 이미지 파일 배치

```
ppt/media/image1.png
```

### 2. Content_Types.xml 업데이트

```xml
<Default Extension="png" ContentType="image/png"/>
```

### 3. 슬라이드 관계 파일 업데이트

`ppt/slides/_rels/slide1.xml.rels`:

```xml
<Relationship Id="rId2"
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
  Target="../media/image1.png"/>
```

### 4. 슬라이드에 이미지 요소 추가

```xml
<p:pic>
  <p:nvPicPr>
    <p:cNvPr id="4" name="Picture 1"/>
    <p:cNvPicPr>
      <a:picLocks noChangeAspect="1"/>
    </p:cNvPicPr>
    <p:nvPr/>
  </p:nvPicPr>

  <p:blipFill>
    <a:blip r:embed="rId2"/>  <!-- 관계 ID 참조 -->
    <a:stretch>
      <a:fillRect/>
    </a:stretch>
  </p:blipFill>

  <p:spPr>
    <a:xfrm>
      <a:off x="914400" y="914400"/>
      <a:ext cx="4572000" cy="3429000"/>
    </a:xfrm>
    <a:prstGeom prst="rect">
      <a:avLst/>
    </a:prstGeom>
  </p:spPr>
</p:pic>
```

## 슬라이드 추가

새 슬라이드 추가 시 수정해야 할 파일들:

### 1. 슬라이드 XML 생성

`ppt/slides/slide3.xml` 생성

### 2. 슬라이드 관계 파일 생성

`ppt/slides/_rels/slide3.xml.rels`:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
    Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"
    Target="../slideLayouts/slideLayout2.xml"/>
</Relationships>
```

### 3. presentation.xml 업데이트

슬라이드 ID 목록에 추가:

```xml
<p:sldIdLst>
  <p:sldId id="256" r:id="rId2"/>
  <p:sldId id="257" r:id="rId3"/>
  <p:sldId id="258" r:id="rId4"/>  <!-- 새 슬라이드 -->
</p:sldIdLst>
```

### 4. presentation.xml.rels 업데이트

```xml
<Relationship Id="rId4"
  Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide"
  Target="slides/slide3.xml"/>
```

### 5. [Content_Types].xml 업데이트

```xml
<Override PartName="/ppt/slides/slide3.xml"
  ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
```

### 6. docProps/app.xml 업데이트

슬라이드 수 증가:

```xml
<Slides>3</Slides>
```

## 슬라이드 삭제

삭제 시 정리해야 할 항목들:

1. `ppt/slides/slideN.xml` 삭제
2. `ppt/slides/_rels/slideN.xml.rels` 삭제
3. `presentation.xml`에서 `<p:sldId>` 제거
4. `presentation.xml.rels`에서 관계 제거
5. `[Content_Types].xml`에서 Override 제거
6. 연결된 미디어 파일 삭제 (다른 곳에서 사용하지 않는 경우)
7. `docProps/app.xml` 슬라이드 수 감소

## 테마 편집

### theme1.xml 구조

```xml
<a:theme name="Custom Theme">
  <a:themeElements>
    <!-- 색상 스킴 -->
    <a:clrScheme name="Custom Colors">
      <a:dk1><a:srgbClr val="1A1A2E"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="16213E"/></a:dk2>
      <a:lt2><a:srgbClr val="F5F5F5"/></a:lt2>
      <a:accent1><a:srgbClr val="E94560"/></a:accent1>
      <a:accent2><a:srgbClr val="FF6B35"/></a:accent2>
      <a:accent3><a:srgbClr val="FCBF49"/></a:accent3>
      <a:accent4><a:srgbClr val="00D4FF"/></a:accent4>
      <a:accent5><a:srgbClr val="7B2CBF"/></a:accent5>
      <a:accent6><a:srgbClr val="004E89"/></a:accent6>
      <a:hlink><a:srgbClr val="0077B6"/></a:hlink>
      <a:folHlink><a:srgbClr val="7B2CBF"/></a:folHlink>
    </a:clrScheme>

    <!-- 폰트 스킴 -->
    <a:fontScheme name="Custom Fonts">
      <a:majorFont>
        <a:latin typeface="Bebas Neue"/>
        <a:ea typeface="Malgun Gothic"/>
      </a:majorFont>
      <a:minorFont>
        <a:latin typeface="Arial"/>
        <a:ea typeface="Malgun Gothic"/>
      </a:minorFont>
    </a:fontScheme>
  </a:themeElements>
</a:theme>
```

## 스크립트

### 언팩

```bash
python ooxml/scripts/unpack.py input.pptx ./unpacked/
```

### 리팩

```bash
python ooxml/scripts/pack.py ./unpacked/ output.pptx
```

### 검증

```bash
python ooxml/scripts/validate.py output.pptx
```

## 일반적인 오류와 해결

### 1. 파일이 열리지 않음

```
원인: XML 구조 오류, 누락된 관계
해결: validate.py 실행 후 오류 수정
```

### 2. 이미지가 표시되지 않음

```
원인: 관계 ID 불일치, Content_Types 누락
해결: rId와 실제 관계 파일 확인
```

### 3. 텍스트 깨짐

```
원인: 인코딩 문제, 폰트 미설치
해결: UTF-8 인코딩 확인, 시스템 폰트 사용
```

### 4. 슬라이드 순서 문제

```
원인: sldIdLst 순서 불일치
해결: presentation.xml의 슬라이드 ID 순서 확인
```

## 검증 체크리스트

- [ ] 모든 관계 ID가 유효한 파일을 참조
- [ ] Content_Types에 모든 파일 타입 선언
- [ ] 슬라이드 ID가 연속적
- [ ] 미사용 미디어 파일 없음
- [ ] XML 문법 오류 없음
- [ ] 폰트가 시스템에 설치되어 있거나 내장됨
