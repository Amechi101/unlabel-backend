import domready from 'domready'
import Gallery from './components/gallery'

class App {
  constructor() {
    console.log('[Unlabel App]')

    this.initComponents()
  }
  initComponents() {
    // Gallery
    const galleries_arr = [].slice.call(document.querySelectorAll('.gallery'))
    galleries_arr.forEach((gallery_el) => {
      new Gallery({
        el: gallery_el
      })
    })
  }
}

domready(() => {
  new App()
})