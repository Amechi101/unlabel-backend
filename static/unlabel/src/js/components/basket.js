import closest from 'closest'

class Basket {
  constructor() {
    this.addEvents()
  }
  addEvents() {
    document.body.addEventListener('click', (e) => {
      if( e.target.matches('.quantity__btn--less') ){
        this.handleBtnModifyQuantity(e, -1)
      } else if( e.target.matches('.quantity__btn--more') ) {
        this.handleBtnModifyQuantity(e, +1)
      }
    })

    document.body.addEventListener('change', (e) => {
      if( e.target.matches('.quantity__select') ){
        this.handleSelectModifyQuantity(e)
      }
    })
  }
  handleBtnModifyQuantity(e, step) {
    e.stopImmediatePropagation()
    e.preventDefault()

    const basketItem_el = closest(e.target, '.basket-item')
    const basketItem_quantityInput_el = basketItem_el.querySelector('.basket-item__quantityInput')
    const basketItem_quantitySubmit_el = basketItem_el.querySelector('.basket-item__quantitySubmit')
    
    basketItem_quantityInput_el.value = parseInt(basketItem_quantityInput_el.value) + step
    basketItem_quantitySubmit_el.click()
  }
  handleSelectModifyQuantity(e) {
    e.preventDefault()

    const basketItem_el = closest(e.target, '.basket-item')
    const basketItem_quantityInput_el = basketItem_el.querySelector('.basket-item__quantityInput')
    const basketItem_quantitySubmit_el = basketItem_el.querySelector('.basket-item__quantitySubmit')
    
    basketItem_quantityInput_el.value = parseInt(e.target.value)
    basketItem_quantitySubmit_el.click()
  }
}

module.exports = Basket