FROM php:8.4-cli

RUN apt-get update && apt-get install -y \
  unzip \
  curl \
  libcurl4-openssl-dev \
  libzip-dev \
  && docker-php-ext-install sockets zip curl

RUN docker-php-ext-install sockets zip

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /var/www/html

COPY . .

RUN composer install

CMD ["php", "-S", "0.0.0.0:8000", "-t", "public"]
