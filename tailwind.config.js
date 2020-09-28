module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {
      spacing: {
        // doc에 없을때 만들면된다!! 0.3이런 숫자 업스면!!
        // 왼쪽은 class name이고..(입력값. class안에!) 오른쪽은 css값이다!
        "5vh": "5vh",
        "10vh": "10vh",
        "15vh": "15vh",
        "25vh": "25vh",
        "50vh": "50vh",
        "75vh": "75vh",
      },
      borderRadius: {
        xl: "1.5rem"
      },
    },
  },
  variants: {},
  plugins: [],
}