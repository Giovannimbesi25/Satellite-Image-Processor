# Satellite Image Processor

Questo progetto offre un sistema per l'elaborazione di immagini satellitari.
L'applicativo prevede l'inserimento da parte dell'utente delle coordinate geografiche del vertice in alto a sinistra e in basso a destra della regione rettangolare da catturare, il livello di zoom desiderato e il numero di sotto-immagini in cui dividere la regione. Ciascuna sottoimmagine viene spedita ad un servizio consumer per l'analisi cromatica tramite l'utilizzo di RabbitMQ.
L'analisi verte su una semplice classificazione dei pixel in base al colore.

Si ringrazia il progetto [satellite-imagery-downloader](https://github.com/andolg/satellite-imagery-downloader) che permette il download delle immagini satellitari

## Istruzioni

### Build delle immagini Docker

```bash
cd satelliteImageConsumer
docker build -t satellite-image-consumer .
```
```bash
cd satelliteImageSender
docker build -t satellite-image-sender .
```

### Creazione Docker Network 
```bash
docker network create satellite_network
```

### Avvio Container
```bash
docker run --rm --name rabbitmq --network=satellite_network -p 5672:5672 -p 15672:15672 rabbitmq
```
```bash
docker run -t -i --rm --name satellite-image-sender --network=satellite_network satellite-image-sender
```
```bash
docker run -t -i --rm --name satellite-image-consumer --network=satellite_network satellite-image-consumer
```


### Coordinate di esempio

Le seguenti sono coordinate di esempio che possono essere utilizzate per l'esecuzione:
```bash
41.9000,12.4813
```
```bash
41.8919,12.4987
```
    
    

