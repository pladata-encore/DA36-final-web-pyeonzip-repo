
window.onload = function () {
    let savedTab = sessionStorage.getItem("selectedTab") || 'all';
    let savedStore = sessionStorage.getItem("selectedStore") || 'all';
    let savedCategory = sessionStorage.getItem("selectedCategory") || 'all';
    let savedPage= sessionStorage.getItem("selectedPage") || 1 ;

};

function openTab(tab='all') {

    // 모든 버튼에서 active 클래스를 제거
    let tabButtons = document.getElementsByClassName("product-tab-btn");
    console.log(tabButtons)
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("product-btn-primary");
        tabButtons[i].classList.add("btn");

        console.log(tabButtons[i].classList)
    }

    let selectedButton = document.querySelector(`button[onclick="openTab('${tab}')"]`);

    selectedButton.classList.add("product-btn-primary");

    let storeRadio = document.querySelector(`input[name="store"][value="ALL"]`);
    if (storeRadio) {
        storeRadio.checked = true;
    }

    let categoryRadio = document.querySelector(`input[name="category"][value="ALL"]`);
    if (categoryRadio) {
        categoryRadio.checked = true;
    }

    history.pushState(null, '', `/product/main/${tab}/`);
    sessionStorage.setItem("selectedTab", tab);
    // AJAX 요청을 통해 HTML 코드 조각 받아오기
    fetch(`/product/filter_products/ALL/ALL/${tab}/1`)
        .then(response => response.text())
        .then(html => {
            // 선택된 탭에 HTML 코드 삽입
            document.getElementById("product-list").innerHTML = html;
        })
        .catch(error => {
            console.error('Error fetching HTML:', error);
            document.getElementById("product-list").innerHTML = '<p>Failed to load content.</p>';
        });

}

function filterProducts(page=1) {
// 선택된 스토어와 카테고리 값을 가져옴
    const selectedStore = document.querySelector("input[name='store']:checked").value;
    console.log(selectedStore)
    const selectedCategory = document.querySelector("input[name='category']:checked").value;
    tabname=document.getElementsByClassName("product-btn-primary")[0].value;
    // fetch 요청으로 필터링된 제품 가져오기
    history.pushState(null, '', `/product/filter_products/${selectedStore}/${selectedCategory}/${tabname}/${page}`)

    fetch(`/product/filter_products/${selectedStore}/${selectedCategory}/${tabname}/${page}`)
        .then(response => response.text())  // JSON이 아니라 HTML이므로 `.text()` 사용
        .then(html => {
            document.getElementById("product-list").innerHTML = html;


            });
    sessionStorage.setItem("selectedTab", tabname);
    sessionStorage.setItem("selectedStore", selectedStore);
    sessionStorage.setItem("selectedCategory", selectedCategory);
    sessionStorage.setItem("selectedPage",page);
}

if (document.addEventListener) {
  window.addEventListener('pageshow', function(event) {
    if (event.persisted || performance.getEntriesByType("navigation")[0].type === 'back_forward') {
      location.reload();
    }
  }, false);
}


