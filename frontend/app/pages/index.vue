<template>
  <div>
    <NavBar />
    <h1>hello world</h1>
    <div style="display: flex; justify-content: center; margin-top: 20vh;">
      <ul>
        <FetchButton :fetchUrl="'/endpoint/api/test_json'" :showErrModal=true @data-received="openJsonModal">get json!</FetchButton>
        <br>
        <FetchButton :fetchUrl="'/endpoint/api/test_text'" :showErrModal=true @data-received="openTextModal">get text!</FetchButton>
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
</script>
