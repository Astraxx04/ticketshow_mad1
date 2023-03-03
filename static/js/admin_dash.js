//Venue creation
const venuesContainer = document.getElementById("venues-container");

const venueData = [
	{ name: "Venue 1", time: 30, },
	{ name: "Venue 2", time: 25, },
	{ name: "Venue 3", time: 40, }
];
const numVenueToPrint = 3;

for (let i = 0; i < numVenueToPrint; i++) {
	// Create a new card element
	const vcard = document.createElement("div");
	vcard.classList.add("vcard");

	// Add the card data to the element
	const vcardDataIndex = i % venueData.length; // Use modulo to cycle through the data
	const vcardDataItem = venueData[vcardDataIndex];
	vcard.innerHTML = `
		<h1>${vcardDataItem.name}</h1>
        <button onclick='createShows()'>Click me</button>
	`;

	// Add the card element to the card container
	venuesContainer.appendChild(vcard);
}
const vcard = document.createElement("div");
vcard.classList.add("vvcard");
vcard.innerHTML = `<button class="venueadd_button" id="venueadd_button"><img class="add-venue-img" id="add-venue-img" src="../images/plus_icon.png" alt="Add a new Show"></button>`;
// Add the card element to the card container
venuesContainer.appendChild(vcard);





function createShows() {
    //Show creation
    const showsContainer = document.getElementById("shows-container");

    const cardData = [
        { name: "Show 1", time: 30, },
        { name: "Show 2", time: 25, },
        { name: "Show 3", time: 40, }
    ];
    const numCardsToPrint = 5;

    for (let i = 0; i < numCardsToPrint; i++) {
        // Create a new card element
        const card = document.createElement("div");
        card.classList.add("card");
        card.id="card-cont";

        // Add the card data to the element
        const cardDataIndex = i % cardData.length; // Use modulo to cycle through the data
        const cardDataItem = cardData[cardDataIndex];
        card.innerHTML = `
            <h2>${cardDataItem.name}</h2>
            <p>Timings: ${cardDataItem.time}</p>
            <button class="actions_button" id="actions_button">Actions</button>
        `;

        // Add the card element to the card container
        showsContainer.appendChild(card);
    }
    const card = document.createElement("div");
    card.classList.add("card");
    card.innerHTML = `<button class="showadd_button" id="showadd_button"><img class="add-show-img" id="add-show-img" src="../images/plus_icon.png" alt="Add a new Show"></button>`;
    // Add the card element to the card container
    showsContainer.appendChild(card);
}


