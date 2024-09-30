function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
  }
  (function () {
    const btnEliminacion = document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Seguro que deseas eliminar este producto?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
})();
(function () {
  const btnConfirmacion = document.querySelectorAll(".btnConfirmacion");

  btnConfirmacion.forEach(btn => {
      btn.addEventListener('click', (e) => {
          const confirmacion = confirm('¿Seguro que deseas agregar este producto?');
          if (!confirmacion) {
              e.preventDefault();
          }
      });
  });
})();


  const productContainers = [...document.querySelectorAll('.product-container')];
  const nxtBtn = [...document.querySelectorAll('.nxt-btn')];
  const preBtn = [...document.querySelectorAll('.pre-btn')];


  productContainers.forEach((item, i) => {
      let containerDimensions = item.getBoundingClientRect();
      let containerWidth = containerDimensions.width;
  
      nxtBtn[i].addEventListener('click', () => {
          item.scrollLeft += containerWidth;
      })
  
      preBtn[i].addEventListener('click', () => {
          item.scrollLeft -= containerWidth;
      })
  })

  const imgs = document.querySelectorAll('.img-select a');
  const imgBtns = [...imgs];
  let imgId = 1;
  
  imgBtns.forEach((imgItem) => {
      imgItem.addEventListener('click', (event) => {
          event.preventDefault();
          imgId = imgItem.dataset.id;
          slideImage();
      });
  });
  
  function slideImage(){
      const displayWidth = document.querySelector('.img-showcase img:first-child').clientWidth;
  
      document.querySelector('.img-showcase').style.transform = `translateX(${- (imgId - 1) * displayWidth}px)`;
  }
  
  window.addEventListener('resize', slideImage);
  function myFunction() {
      var x = document.getElementById("myTopnav");
      if (x.className === "topnav") {
        x.className += " responsive";
      } else {
        x.className = "topnav";
      }
    }



    function replaceButton() {
      var button = document.getElementById('myButton');
      var replacementDiv = document.getElementById('replacementDiv');
      var displayText = document.getElementById('displayText');
      
      button.classList.add('hidden');
      replacementDiv.classList.remove('hidden');
      displayText.classList.add('hidden');
    }

    function hideDiv() {
      var button = document.getElementById('myButton');
      var replacementDiv = document.getElementById('replacementDiv');
      var displayText = document.getElementById('displayText');
      
      button.classList.remove('hidden');
      replacementDiv.classList.add('hidden');
      displayText.classList.remove('hidden');
    }

    function iniciarMap(){
      var coord = {lat:-33.361320 ,lng: -70.734677};
      var map = new google.maps.Map(document.getElementById('map'),{
        zoom: 10,
        center: coord
      });
      var marker = new google.maps.Marker({
        position: coord,
        map: map
      });
  }