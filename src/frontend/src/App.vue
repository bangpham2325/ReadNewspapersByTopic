<template>
  <router-view :key="$route.params.name"/>
</template>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap');

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-family: 'Roboto', sans-serif;
  font-size: 20px;
  font-weight: 300;
  color: #000000;
  margin: 0 auto;
  background-color: #F5F5F5;
  min-height: 100vh;
}

*{
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

$menu-item-active-color: #FFFFFF;
$menu-item-hover-color: #FFFFFF;
$menu-item-active-background-color: #024547;
$menu-item-hover-background-color: #024547;
$input-border-color: #eee;
$input-hover-border-color: #eee;
$input-focus-border-color: #eee;
$input-focus-box-shadow-color: #eee;
@import "../node_modules/bulma";
</style>
