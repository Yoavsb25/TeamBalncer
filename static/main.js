$(document).ready(function() {
    // Initial setup: load home content
    $('#content').load('home.html');

    // Handle navigation clicks
    $('#home-link').click(function(e) {
        e.preventDefault();
        $('#content').load('home.html');
    });

    $('#create-teams-link').click(function(e) {
        e.preventDefault();
        $('#content').load('create_teams.html');
    });

    $('#create-players-link').click(function(e) {
        e.preventDefault();
        $('#content').load('create_players.html');
    });
});
