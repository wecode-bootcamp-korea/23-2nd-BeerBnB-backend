## 🍻비어비앤비 프로젝트 소개
<div align=center><img src="https://i.ibb.co/yY0WNZF/Screen-Shot-2021-08-26-at-9-21-59-PM.png"></div>

**<div align=center> 비어비앤비 클론 프로젝트</div>**
<div align=center> 짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인/기획 부분만 클론했습니다.<br>
개발은 초기 세팅부터 전부 직접 구현했으며, 아래 데모 영상에서 보이는 부분은<br>
모두 백앤드와 연결하여 실제 사용할 수 있는 서비스 수준으로 개발한 것입니다.<br></div>

<br>

## 개발 인원 및 기간

- 개발기간 : 2021/8/17(화) ~ 2021/8/27 (금)
- 개발 인원 : 프론트엔드 4명 (김가영, 배윤아, 이나현, 황문실)
           백엔드 2명 (김도담, 박종규)

<br>

## Modeling✏️
![](https://i.ibb.co/bNwHSXy/2021-08-26-9-12-25.png)

상기 모델링 중에서 User, Booking, Product, Category를 구현했습니다.

## 구현 페이지

### [시연 영상](https://www.youtube.com/watch?v=ecPMjOMoKWY)

### 메인 페이지
![메인페이지](https://user-images.githubusercontent.com/81546305/131219959-a409451d-e6a6-4388-8936-a611a41d7882.gif)


### 호스트 되기 (숙소 등록)
![호스트되기](https://user-images.githubusercontent.com/81546305/131219980-c6e26913-577a-4c92-a5b9-eb24498777b9.gif)


### 상품 검색
![상품검색](https://user-images.githubusercontent.com/81546305/131219985-f9282f03-421e-41dd-875b-d185f20cfb93.gif)

### 상품 리스트
![상품리스트](https://user-images.githubusercontent.com/81546305/131219992-006f527f-2b20-47eb-bf2e-e0724cb27c12.gif)

### 상세 페이지 / 예약 하기
![상세페이지예약](https://user-images.githubusercontent.com/81546305/131220015-e76d901d-6a7b-4220-8d09-17a485fe585a.gif)


### 소셜 로그인
![ezgif com-gif-maker (2)](https://user-images.githubusercontent.com/81546305/131218610-cef2bd34-6899-47f2-8113-0a15e0a64625.gif)

### 예약 확인
![마이페이지로그아웃](https://user-images.githubusercontent.com/81546305/131220022-2b26c9dc-4db2-42a1-8575-2bba23751896.gif)


## **구현기능💻**


### **User**

- 카카오 소셜 로그인
- 프론트 단에서 카카오 토큰을 받아 서버 토큰으로 반환
- 기존에 등록되어 있는 회원 정보(닉네임, 프로필 사진)는 카카오 기반으로 업데이트
- 로그인 데코레이터


### **Product**

- quary parameter를 이용한 상품 필터링(주소, 체크인, 체크아웃, 인원)
- 상품 상세 정보 및 예약 가능 일자 확인
- 호스트 되기 상품 등록

### **Booking**

- 숙소 예약 기능 구현
- 내가 예약한 숙소 확인
- 내가 등록한 숙소의 예약 현황 확인

<br>
              
예약 사이트의 기본적인 기능들을 다루며 전반적인 플로우와 소셜 로그인의 프로세스를 배울 수 있었습니다.<br>
또한 query debugger로 ORM를 최적화했으며 unit test로 클린한 코드 작성을 위해 노력했습니다. <br>

<br>

## **사용 기술👍**

Backend : Python, Django, MySql, AWS EC2, AWS RDS, Docker


<br>

## **커뮤니케이션🤝**

비어비앤비 팀은 3개의 Tool을 이용해서 원활한 커뮤니케이션 문화를 형성했습니다

<br>

### Trello
![](https://i.ibb.co/zGnK83C/2021-08-26-9-20-45.png)

- Front/Back로 라벨을 분류하고, 티켓 담당자를 표기해서 직관적으로 확인
- 미팅 기록을 간략하게 정리해서 로그에 저장
- 원활한 프-백간 통신을 위해 IP 주소는 메일 업데이트

<br>

### [Google Slides(Sketch)](https://docs.google.com/presentation/d/1vEYF9QDYuJZ6oQgHwR1JIhM-XRTplibJfl1MvWDJhrM/edit?usp=sharing)

- 각 페이지별 컴포넌트 분류하여 간략하게 도식화
- 컴포넌트마다 어떤 위치에 어떤 API를 사용하는지 직관적으로 확인 가능

<br>

### [Google Spreadsheet(API정의서)](https://docs.google.com/spreadsheets/d/1wM0Sy5hMKLhlHufnKBXtfgCo_7BfDpABbiwFxpHlB7w/edit?usp=sharing)

- API별 기능, Method, URI, Request 및 Response 정리
<br>

### Reference

- 이 프로젝트는 비어비앤비 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
