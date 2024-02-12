<template>
  <div>
    <input class="form-control" list="datalistOptions" id="exampleDataList" 
            placeholder="User to search..." v-model="searchQuery" @input="searchUsers">
    <datalist id="datalistOptions">
      <option v-for="result in searchResults" :value="result.name" :key="result.id"></option>
    </datalist>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      selectedUser: null,
      showResults: false,
      error: '',
    };
  },
  methods: {
    async searchUsers() {
      if (this.searchQuery.trim() === '') {
        this.showResults = false;
        return;
      }

      try {
        const response = await fetch(`/endpoint/user/search/?search=${this.searchQuery}`);
        // console.log(response);
        if (response.ok) {
          const data = await response.json();
          // console.log(data)
          this.searchResults = data;
          this.showResults = true;
        } else {
          console.error('Error searching users:', response.statusText);
        }
      } catch (error) {
        console.error('Error searching users:', error);
      }
    },
    selectUser(user) {
      this.selectedUser = user;
      this.showResults = false;
      //TODO: Do something with the selected user, e.g., emit an event or update parent component state
    },
  },
};
</script>
