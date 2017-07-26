# Unlabel - Frontend

## Requirements
- [Node](https://docs.npmjs.com/getting-started/what-is-npm)

## Install
```
	npm install # install all dependencies
```

## Develop
```
	npm run dev # compile css and js files for development and start a local server with hot-reloading proxying (127.0.0.1:8000)[http://127.0.0.1:8000/]
```

### CSS
The css files are written in (Stylus)[http://stylus-lang.com/] and following the (ITCSS)[https://www.xfive.co/blog/itcss-scalable-maintainable-css-architecture/] architecture and (BEM)[http://getbem.com/] naming convention


### Icons
Exported in svg from Sketch and bundled in a webfont using (icomoon)[http://icomoon.io]. The webfont configuration can be found in `./src/icons`.

## Deploy
```
	npm run prod # compile and compress css and js files for production

```