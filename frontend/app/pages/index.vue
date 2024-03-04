<template>
  <div style="margin: auto; text-wrap: wrap; overflow:hidden; align-self: center;">
    <h1 style="font-size: 4vw;">Welcome to FT_TRANSCENDENCE</h1>
  </div>
</template>

<script>
export default {
  data() {
    return {
    };
  },
  methods: {
  },
};
</script>

<!-- <template>
  <div>
    <h1>hello world</h1>
    <div style="display: flex; justify-content: center; margin-top: 20vh;">
      <ul>
        <FetchButton :fetchUrl="'/endpoint/api/test_json'" :showErrModal=true @data-received="openJsonModal">get json!</FetchButton>
        <br>
        <FetchButton :fetchUrl="'/endpoint/user/info/'" :showErrModal=true @data-received="openTextModal">get text!</FetchButton>
        <br>
      </ul>
    </div>
    <SimpleModal v-show="modalContent" :content="modalContent" :modalTitle="'Response:'" modalId="exampleModal" ariaLabel="A simple modal to show html content" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      modalContent: null,
    };
  },
  methods: {
    openJsonModal(data) {
      this.modalContent = Object.entries(data)
        .map(([key, value]) => `${key}: ${value}`)
        .join('<br>');
      this.$nextTick(() => {
        new bootstrap.Modal(document.getElementById('exampleModal')).show();
      });
    },
    openTextModal(data) {
      this.modalContent = data;
      this.$nextTick(() => {
        new bootstrap.Modal(document.getElementById('exampleModal')).show();
      });
    },
  },
};
</script> -->