const gulp = require("gulp");

const css = () => {
  const postCSS = require("gulp-postcss");
  const sass = require("gulp-sass");
  const minify = require("gulp-csso");
  sass.compiler = require("node-sass");
  return gulp
    .src("assets/scss/styles.scss")
    // 이 파일을 쓸것이고
    .pipe(sass().on("error", sass.logError))
    .pipe(postCSS([require("tailwindcss"), require("autoprefixer")]))
    // 두가지 require을 쓸것이고
    .pipe(minify())
    // 모든 아웃풋을 minify 할것이고
    .pipe(gulp.dest("static/css"));
}; // 결과물을 static/css에 넣을것임!

exports.default = css;