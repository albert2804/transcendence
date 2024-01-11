<!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
  Launch demo modal
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        ...
        </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>


<script>
  export default {
    name: 'localTournament',
      data() {
        return {
          all_players: [
            {
              name: '',
              games_won: '[]',
            }
          ],
          nbr_players: '',
        }
      },
    mounted() {},
    methods: {

    },
  };
</script>

<style scoped>
.start-tournament{
  margin: 10px auto; /* Center the button horizontally */
  padding: 10px;
  font-size: 16px;
}

</style>